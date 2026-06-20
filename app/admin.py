"""
Minimal built-in admin for the blog: login, write, publish. No external tools,
no separate CMS. A single operator (Paseka) signs in with a password from the
environment, writes a post in a plain form, and chooses Save draft or Publish.

Auth: a session cookie (Starlette SessionMiddleware, configured in main.py)
flags the browser as signed in. There is no user table or password hashing
library here on purpose, this protects one person's own content on one site,
not multiple accounts. Set ADMIN_PASSWORD (and optionally ADMIN_USERNAME) in
.env. If ADMIN_PASSWORD is not set, login is disabled entirely.

Uploads: a cover image and/or a PDF/document attachment can be attached to an
article. Files are saved under app/static/uploads/blog/ with a random name
(the original filename is never trusted as a path) and served straight from
the existing /static mount, no extra storage service involved.
"""
import os
import re
import secrets
import uuid
from datetime import date, datetime
from pathlib import Path

from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.database import get_session
from app.models import BlogPost
from app.data import content as C

APP_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = APP_DIR / "static" / "uploads" / "blog"
UPLOAD_URL_PREFIX = "/static/uploads/blog"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt", ".csv"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024
MAX_DOCUMENT_BYTES = 20 * 1024 * 1024

templates = Jinja2Templates(directory=str(APP_DIR / "templates"))
templates.env.globals.update(SITE=C.SITE)

router = APIRouter(prefix="/admin", tags=["admin"])


def admin_page(request: Request, template: str, **ctx) -> HTMLResponse:
    return templates.TemplateResponse(request, f"admin/{template}", ctx)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "post"


def unique_slug(db: Session, base_slug: str, exclude_id: int | None = None) -> str:
    slug = base_slug
    suffix = 2
    while True:
        existing = db.exec(select(BlogPost).where(BlogPost.slug == slug)).first()
        if not existing or existing.id == exclude_id:
            return slug
        slug = f"{base_slug}-{suffix}"
        suffix += 1


def require_admin(request: Request) -> None:
    if not request.session.get("admin"):
        raise HTTPException(status_code=303, headers={"Location": "/admin/login"})


class UploadError(Exception):
    pass


def save_upload(file: UploadFile | None, *, allowed_ext: set[str], max_bytes: int, kind: str) -> tuple[str, str] | None:
    """Validate and store an optional upload. Returns (url_path, original_filename),
    or None if no file was actually chosen. Raises UploadError with a message
    that is safe to show the admin directly."""
    if file is None or not file.filename:
        return None

    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_ext:
        allowed = ", ".join(sorted(allowed_ext))
        raise UploadError(f"{kind}: \"{ext or 'unknown'}\" is not allowed. Use one of: {allowed}")

    content = file.file.read()
    if not content:
        return None
    if len(content) > max_bytes:
        raise UploadError(f"{kind}: file is too large (max {max_bytes // (1024 * 1024)} MB)")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex[:12]}{ext}"
    (UPLOAD_DIR / stored_name).write_bytes(content)
    return f"{UPLOAD_URL_PREFIX}/{stored_name}", file.filename


def delete_upload_file(url_path: str | None) -> None:
    """Best-effort cleanup of a previously uploaded file when it is replaced
    or removed. Never raises, a missing file on disk is not an error here."""
    if not url_path or not url_path.startswith(UPLOAD_URL_PREFIX):
        return
    try:
        (UPLOAD_DIR / Path(url_path).name).unlink(missing_ok=True)
    except OSError:
        pass


# --------------------------------------------------------------------------- #
#  Login / logout
# --------------------------------------------------------------------------- #
@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_form(request: Request):
    if request.session.get("admin"):
        return RedirectResponse("/admin", status_code=303)
    return admin_page(request, "login.html", error=None)


@router.post("/login", response_class=HTMLResponse, include_in_schema=False)
def login_submit(request: Request, username: str = Form(""), password: str = Form("")):
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_username = os.getenv("ADMIN_USERNAME", "admin")

    if not admin_password:
        return admin_page(
            request, "login.html",
            error="Admin login is not configured. Set ADMIN_PASSWORD in .env to enable it.",
        )

    username_ok = secrets.compare_digest(username.strip(), admin_username)
    password_ok = secrets.compare_digest(password, admin_password)
    if not (username_ok and password_ok):
        return admin_page(request, "login.html", error="Incorrect username or password.")

    request.session["admin"] = True
    return RedirectResponse("/admin", status_code=303)


@router.get("/logout", include_in_schema=False)
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin/login", status_code=303)


# --------------------------------------------------------------------------- #
#  Dashboard
# --------------------------------------------------------------------------- #
@router.get("", response_class=HTMLResponse, dependencies=[Depends(require_admin)], include_in_schema=False)
def dashboard(request: Request, db: Session = Depends(get_session)):
    posts = db.exec(select(BlogPost).order_by(BlogPost.published.desc())).all()
    return admin_page(request, "dashboard.html", posts=posts)


# --------------------------------------------------------------------------- #
#  Write / publish
# --------------------------------------------------------------------------- #
@router.get("/posts/new", response_class=HTMLResponse, dependencies=[Depends(require_admin)], include_in_schema=False)
def new_post_form(request: Request):
    return admin_page(request, "post_form.html", post=None, today=date.today().isoformat())


@router.post("/posts/new", response_class=HTMLResponse, dependencies=[Depends(require_admin)], include_in_schema=False)
def create_post(
    request: Request,
    title: str = Form(...),
    slug: str = Form(""),
    category: str = Form(...),
    excerpt: str = Form(...),
    body: str = Form(...),
    published: str = Form(...),
    action: str = Form("draft"),
    image: UploadFile | None = File(None),
    attachment: UploadFile | None = File(None),
    db: Session = Depends(get_session),
):
    try:
        image_result = save_upload(image, allowed_ext=IMAGE_EXTENSIONS, max_bytes=MAX_IMAGE_BYTES, kind="Cover image")
        attachment_result = save_upload(attachment, allowed_ext=DOCUMENT_EXTENSIONS, max_bytes=MAX_DOCUMENT_BYTES, kind="Attachment")
    except UploadError as exc:
        return admin_page(request, "post_form.html", post=None, today=date.today().isoformat(), error=str(exc))

    base_slug = slugify(slug or title)
    post = BlogPost(
        slug=unique_slug(db, base_slug),
        title=title.strip(),
        category=category.strip(),
        excerpt=excerpt.strip(),
        body=body.strip(),
        published=datetime.strptime(published, "%Y-%m-%d").date(),
        is_published=(action == "publish"),
        image_path=image_result[0] if image_result else None,
        attachment_path=attachment_result[0] if attachment_result else None,
        attachment_name=attachment_result[1] if attachment_result else None,
    )
    db.add(post)
    db.commit()
    return RedirectResponse("/admin", status_code=303)


@router.get("/posts/{post_id}/edit", response_class=HTMLResponse, dependencies=[Depends(require_admin)], include_in_schema=False)
def edit_post_form(request: Request, post_id: int, db: Session = Depends(get_session)):
    post = db.get(BlogPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return admin_page(request, "post_form.html", post=post, today=date.today().isoformat())


@router.post("/posts/{post_id}/edit", response_class=HTMLResponse, dependencies=[Depends(require_admin)], include_in_schema=False)
def update_post(
    request: Request,
    post_id: int,
    title: str = Form(...),
    slug: str = Form(""),
    category: str = Form(...),
    excerpt: str = Form(...),
    body: str = Form(...),
    published: str = Form(...),
    action: str = Form("draft"),
    remove_image: str = Form(""),
    remove_attachment: str = Form(""),
    image: UploadFile | None = File(None),
    attachment: UploadFile | None = File(None),
    db: Session = Depends(get_session),
):
    post = db.get(BlogPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    try:
        image_result = save_upload(image, allowed_ext=IMAGE_EXTENSIONS, max_bytes=MAX_IMAGE_BYTES, kind="Cover image")
        attachment_result = save_upload(attachment, allowed_ext=DOCUMENT_EXTENSIONS, max_bytes=MAX_DOCUMENT_BYTES, kind="Attachment")
    except UploadError as exc:
        return admin_page(request, "post_form.html", post=post, today=date.today().isoformat(), error=str(exc))

    base_slug = slugify(slug or title)
    post.slug = unique_slug(db, base_slug, exclude_id=post.id)
    post.title = title.strip()
    post.category = category.strip()
    post.excerpt = excerpt.strip()
    post.body = body.strip()
    post.published = datetime.strptime(published, "%Y-%m-%d").date()
    post.is_published = (action == "publish")

    if image_result:
        delete_upload_file(post.image_path)
        post.image_path = image_result[0]
    elif remove_image == "on":
        delete_upload_file(post.image_path)
        post.image_path = None

    if attachment_result:
        delete_upload_file(post.attachment_path)
        post.attachment_path, post.attachment_name = attachment_result
    elif remove_attachment == "on":
        delete_upload_file(post.attachment_path)
        post.attachment_path = None
        post.attachment_name = None

    db.add(post)
    db.commit()
    return RedirectResponse("/admin", status_code=303)


@router.post("/posts/{post_id}/delete", dependencies=[Depends(require_admin)], include_in_schema=False)
def delete_post(post_id: int, db: Session = Depends(get_session)):
    post = db.get(BlogPost, post_id)
    if post:
        delete_upload_file(post.image_path)
        delete_upload_file(post.attachment_path)
        db.delete(post)
        db.commit()
    return RedirectResponse("/admin", status_code=303)
