"""
FastAPI application.

Run from the project root with:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000
"""
from contextlib import asynccontextmanager
import json
import logging
import os
import random
import secrets
from pathlib import Path
import smtplib
from email.message import EmailMessage
from urllib.parse import quote

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
from sqlmodel import Session, select

from app.database import init_db, get_session
from app.models import SampleCourse, QuizQuestion, BlogPost, Lead
from app.data import content as C
from app.assets import asset_version
from app import seed, seo, admin

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
templates.env.globals["asset_version"] = asset_version
logger = logging.getLogger(__name__)

# Jinja's built-in urlencode leaves "/" unescaped, which is fine for query
# strings in general but not for a full URL embedded as a single query VALUE
# (e.g. the social share links on a blog post). Override it to fully
# percent-encode, matching JavaScript's encodeURIComponent.
templates.env.filters["urlencode"] = lambda value: quote(str(value), safe="")


def load_local_env() -> None:
    for env_name in (".env", ".env.local"):
        env_path = PROJECT_DIR / env_name
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


# Loaded at import time (not just on startup) so the session secret and admin
# credentials are available the moment the middleware below is configured.
load_local_env()

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
if not SESSION_SECRET_KEY:
    SESSION_SECRET_KEY = secrets.token_hex(32)
    logger.warning(
        "SESSION_SECRET_KEY not set, generated a temporary one. Admin sessions "
        "will not survive a restart. Set SESSION_SECRET_KEY in .env for production."
    )

UI_LABELS = {
    "en": {
        "back_to_samples": "All sample courses",
        "interactive_sample": "Interactive sample",
        "audience": "Audience",
        "duration": "Duration",
        "outcomes_heading": "What you will be able to do",
        "infographic_badge": "Visual data block",
        "flip_heading": "Reflect and flip",
        "flip_intro": "Each card starts with a prompt. Flip it to reveal the coaching cue or model answer.",
        "flip_prompt": "Prompt",
        "flip_answer": "Answer frame",
        "flip_cta": "Flip for reflection",
        "flip_back": "Flip back",
        "content_heading": "Course content",
        "knowledge_check": "Knowledge check",
        "answered": "answered",
        "quiz_intro": "Answer each question.",
        "correct": "Correct",
        "not_quite": "Not quite",
        "why": "Why:",
        "score_prefix": "You scored",
        "score_suffix": "",
        "score_text": "This is the kind of immediate, low stakes feedback that keeps learners moving. Every sample course is built the same way: outcomes first, then practice, then feedback.",
        "contact_cta": "Request a course like this",
        "select_all": "Select all that apply",
        "submit_answer": "Submit answer",
        "check_answer": "Check my answer",
        "type_answer_placeholder": "Your answer",
        "evaluate_statement": "Evaluate this statement",
        "drag_or_choose": "Drag each item on the right onto its match on the left, or choose it from the dropdown.",
        "drag_or_buttons": "Drag to reorder, or use the up/down buttons.",
        "your_answer": "Your answer",
        "accepted_answers": "Accepted answer(s)",
        "your_order": "Your order",
        "correct_order": "Correct order",
        "missed": "missed",
        "move_up": "Move up",
        "move_down": "Move down",
        "choose_or_drag": "— choose or drag here —",
    },
    "fr": {
        "back_to_samples": "Tous les cours exemples",
        "interactive_sample": "Exemple interactif",
        "audience": "Public",
        "duration": "Duree",
        "outcomes_heading": "Ce que vous saurez faire",
        "infographic_badge": "Bloc visuel",
        "flip_heading": "Reflechir et retourner",
        "flip_intro": "Chaque carte commence par une question. Retournez-la pour voir la piste de reponse ou le modele de reponse.",
        "flip_prompt": "Question",
        "flip_answer": "Piste de reponse",
        "flip_cta": "Retourner pour reflechir",
        "flip_back": "Retourner",
        "content_heading": "Contenu du cours",
        "knowledge_check": "Verification des acquis",
        "answered": "repondues",
        "quiz_intro": "Repondez a chaque question. La correction est faite cote serveur et la bonne reponse n'est pas envoyee au navigateur a l'avance.",
        "correct": "Correct",
        "not_quite": "Pas encore",
        "why": "Pourquoi :",
        "score_prefix": "Votre score est de",
        "score_suffix": "",
        "score_text": "Ce type de retour immediat et sans enjeu excessif aide les apprenants a poursuivre. Chaque cours exemple suit la meme logique : objectifs, pratique, puis feedback.",
        "contact_cta": "Demander un cours similaire",
    },
    "pt": {
        "back_to_samples": "Todos os cursos de exemplo",
        "interactive_sample": "Exemplo interativo",
        "audience": "Publico",
        "duration": "Duracao",
        "outcomes_heading": "O que sera capaz de fazer",
        "infographic_badge": "Bloco visual",
        "flip_heading": "Refletir e virar",
        "flip_intro": "Cada cartao comeca com uma pergunta. Vire-o para ver a orientacao ou a resposta-modelo.",
        "flip_prompt": "Pergunta",
        "flip_answer": "Orientacao",
        "flip_cta": "Virar para refletir",
        "flip_back": "Virar novamente",
        "content_heading": "Conteudo do curso",
        "knowledge_check": "Verificacao de conhecimentos",
        "answered": "respondidas",
        "quiz_intro": "Responda a cada pergunta. A avaliacao acontece no servidor e a resposta correta nao e enviada antecipadamente ao navegador.",
        "correct": "Correto",
        "not_quite": "Ainda nao",
        "why": "Por que:",
        "score_prefix": "A sua pontuacao foi",
        "score_suffix": "",
        "score_text": "Este tipo de feedback imediato e de baixo risco ajuda o formando a continuar. Cada curso de exemplo segue a mesma estrutura: objetivos, pratica e depois feedback.",
        "contact_cta": "Pedir um curso como este",
    },
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed.run()          # seeds only if empty
    yield


app = FastAPI(title="Paseka eLearning", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY, max_age=60 * 60 * 12)
# Compresses text responses (HTML/CSS/JS/SVG). The animated logo SVGs in
# particular are large (dense chalk-texture letterforms), gzip cuts them by
# roughly two thirds over the wire.
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def cache_static_assets(request: Request, call_next):
    """Every /static/* URL is content-hash versioned (see app/assets.py,
    asset_version()), so the same URL is guaranteed to always be the same
    bytes. Safe to tell browsers and any CDN in front of this app to cache it
    for a year without revalidating, repeat visits re-download nothing for
    assets that haven't changed, and instantly pick up ones that have (since
    a content change means a different URL)."""
    response = await call_next(request)
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return response


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(admin.router)

# Make site wide content available to every template.
templates.env.globals.update(SITE=C.SITE, NAV=C.NAV, NAV_SLUGS=C.NAV_SLUGS, SERVICE_MENU=C.SERVICE_MENU)


def page(request: Request, template: str, **ctx) -> HTMLResponse:
    return templates.TemplateResponse(request, template, ctx)


def published_posts(db: Session):
    """Posts visible to the public, newest first. /admin can still see drafts."""
    return db.exec(
        select(BlogPost).where(BlogPost.is_published == True)  # noqa: E712
        .order_by(BlogPost.published.desc())
    ).all()


def send_contact_email(name: str, email: str, country: str, time_zone: str,
                       organisation: str, service: str, message: str,
                       preferred_date: str) -> None:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    recipient = os.getenv("CONTACT_RECIPIENT_EMAIL", C.SITE["email"])
    sender = os.getenv("CONTACT_FROM_EMAIL", smtp_user or recipient)

    if not (smtp_host and smtp_user and smtp_password and recipient):
        logger.info("Contact email not sent, SMTP settings are incomplete.")
        return

    msg = EmailMessage()
    msg["Subject"] = f"New contact submission from {name}"
    msg["From"] = sender
    msg["To"] = recipient
    msg["Reply-To"] = email
    msg.set_content(
        f"New contact form submission\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Country: {country or '-'}\n"
        f"Time zone: {time_zone or '-'}\n"
        f"Organisation: {organisation or '-'}\n"
        f"Service required: {service or '-'}\n"
        f"Preferred consultation date: {preferred_date or '-'}\n\n"
        f"Message:\n{message or '-'}\n"
    )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)


def split_outcomes(text: str) -> list[str]:
    return [line.strip() for line in text.split("\n") if line.strip()]


def parse_course_body(body: str | None) -> list[dict[str, str]]:
    if not body:
        return []

    blocks = []
    for section in body.split("\n\n"):
        text = section.strip()
        if not text:
            continue
        if text.startswith("## "):
            blocks.append({"type": "heading", "text": text[3:].strip()})
        elif text.startswith("**Activity"):
            blocks.append({
                "type": "activity",
                "text": text.replace("**Activity:**", "").replace("**Activity**:", "").strip(),
            })
        elif text.startswith("**Scenario"):
            blocks.append({
                "type": "scenario",
                "text": text.replace("**Scenario:**", "").replace("**Scenario**:", "").strip(),
            })
        elif text.startswith("**Reflection"):
            blocks.append({
                "type": "reflection",
                "text": text.replace("**Reflection:**", "").replace("**Reflection**:", "").strip(),
            })
        else:
            blocks.append({"type": "paragraph", "text": text})
    return blocks


def get_qtype(question_types: list, order: int) -> str:
    return question_types[order] if order < len(question_types) else "pick"


def bitmask_to_set(mask: int) -> set[int]:
    """multi_select reuses the existing `correct: int` column as a 3-bit mask
    (bit i = option i is correct) instead of a single index. No schema change."""
    return {i for i in range(3) if mask & (1 << i)}


def seeded_shuffle(items: list, seed_key: str) -> list:
    """Deterministic shuffle: same seed_key always produces the same order, so
    the display-time shuffle (GET) and scoring-time shuffle (POST) agree
    without persisting any shuffle state server or client side."""
    shuffled = list(items)
    random.Random(seed_key).shuffle(shuffled)
    return shuffled


def build_localized_questions(
    questions: list[QuizQuestion],
    translation: dict | None = None,
    question_types: list | None = None,
) -> list[dict]:
    translated = translation or {}
    qtypes = question_types or []
    localized = []
    translated_questions = translated.get("questions", [])
    for q in questions:
        data = translated_questions[q.order] if q.order < len(translated_questions) else {}
        localized.append({
            "id": q.id,
            "order": q.order,
            "prompt": data.get("prompt", q.prompt),
            "options": [
                data.get("a", q.option_a),
                data.get("b", q.option_b),
                data.get("c", q.option_c),
            ],
            # fill_blank repurposes option_a as a "|"-separated accepted-answer
            # list; this lets a locale override the accepted answer text.
            "accepted": data.get("accepted", q.option_a),
            "explanation": data.get("explanation", q.explanation),
            "correct": q.correct,
            "qtype": get_qtype(qtypes, q.order),
        })
    return localized


def build_synthetic_activities(extras: dict, locale_data: dict | None, base_order: int) -> list[dict]:
    """Matching/sequencing activities don't fit the 3-option QuizQuestion shape,
    so they live purely in seed.py's SAMPLE_EXTRAS (never the DB) and are merged
    in here as synthetic question dicts with string ids, appended after the real
    DB-backed questions. The unanswered dict only ever exposes a shuffled-for-
    display copy -- the canonical order/pairing is never sent before scoring."""
    data = locale_data or {}
    slug = extras.get("slug", "")
    activities = []
    order = base_order

    matching = data.get("matching_activity", extras.get("matching_activity"))
    if matching:
        pairs = matching["pairs"]
        shuffled_right = seeded_shuffle(range(len(pairs)), f"match-{slug}")
        activities.append({
            "id": "matching-0",
            "order": order,
            "qtype": "matching",
            "prompt": matching["prompt"],
            "explanation": matching["explanation"],
            "left_items": [p["left"] for p in pairs],
            "display_right_items": [pairs[i]["right"] for i in shuffled_right],
        })
        order += 1

    sequencing = data.get("sequencing_activity", extras.get("sequencing_activity"))
    if sequencing:
        shuffled_steps = seeded_shuffle(sequencing["steps"], f"sequence-{slug}")
        activities.append({
            "id": "sequencing-0",
            "order": order,
            "qtype": "sequencing",
            "prompt": sequencing["prompt"],
            "explanation": sequencing["explanation"],
            "display_steps": shuffled_steps,
        })
        order += 1

    return activities


def build_course_locales(course: SampleCourse, extras: dict, questions: list[QuizQuestion]) -> dict[str, dict]:
    qtypes = extras.get("question_types", [])
    extras = {**extras, "slug": course.slug}
    locales = {
        "en": {
            "label": "English",
            "title": course.title,
            "summary": course.summary,
            "audience": course.audience,
            "duration": course.duration,
            "outcomes": split_outcomes(course.outcomes),
            "sections": parse_course_body(course.body),
            "preview": extras.get("preview", {}),
            "flip_cards": extras.get("flip_cards", []),
            "infographic": extras.get("infographic", {}),
            "chart": extras.get("chart", {}),
            "questions": (
                build_localized_questions(questions, question_types=qtypes)
                + build_synthetic_activities(extras, None, len(questions))
            ),
            "ui": UI_LABELS["en"],
        }
    }

    for code, data in extras.get("translations", {}).items():
        locales[code] = {
            "label": data.get("label", code.upper()),
            "title": data["title"],
            "summary": data["summary"],
            "audience": data["audience"],
            "duration": data["duration"],
            "outcomes": split_outcomes(data["outcomes"]),
            "sections": parse_course_body(data["body"]),
            "preview": data.get("preview", extras.get("preview", {})),
            "flip_cards": data.get("flip_cards", extras.get("flip_cards", [])),
            "infographic": data.get("infographic", extras.get("infographic", {})),
            "chart": data.get("chart", extras.get("chart", {})),
            "questions": (
                build_localized_questions(questions, data, question_types=qtypes)
                + build_synthetic_activities(extras, data, len(questions))
            ),
            "ui": UI_LABELS.get(code, UI_LABELS["en"]),
        }
    return locales


def get_locale_bundle(course: SampleCourse, extras: dict, questions: list[QuizQuestion], locale: str) -> dict:
    locales = build_course_locales(course, extras, questions)
    return locales.get(locale, locales["en"])


# --------------------------------------------------------------------------- #
#  SEO / GEO: crawler and LLM site maps
# --------------------------------------------------------------------------- #
@app.get("/robots.txt", response_class=PlainTextResponse, include_in_schema=False)
def robots_txt(request: Request):
    return seo.robots_txt(request)


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml(request: Request, db: Session = Depends(get_session)):
    courses = db.exec(select(SampleCourse).order_by(SampleCourse.id)).all()
    posts = published_posts(db)
    return Response(content=seo.sitemap_xml(request, courses, posts),
                    media_type="application/xml")


@app.get("/llms.txt", response_class=PlainTextResponse, include_in_schema=False)
def llms_txt(request: Request, db: Session = Depends(get_session)):
    courses = db.exec(select(SampleCourse).order_by(SampleCourse.id)).all()
    posts = published_posts(db)
    return seo.llms_txt(request, courses, posts)


# --------------------------------------------------------------------------- #
#  Static content pages
# --------------------------------------------------------------------------- #
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    meta, jsonld = seo.home_seo(request)
    return page(request, "index.html",
                value_props=C.VALUE_PROPS, who=C.WHO_I_HELP, faqs=C.FAQS,
                active="Home", meta=meta, jsonld=jsonld)


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    meta, jsonld = seo.about_seo(request)
    return page(request, "about.html", cv=C.CV, active="About", meta=meta, jsonld=jsonld)


@app.get("/services/{slug}", response_class=HTMLResponse)
def service_page(request: Request, slug: str):
    data = C.SERVICE_PAGES.get(slug)
    if not data:
        raise HTTPException(status_code=404, detail="Service not found")
    meta, jsonld = seo.service_seo(request, data, slug)
    return page(request, "service_page.html",
                data=data, slug=slug, frameworks=C.FRAMEWORKS,
                active="Services", meta=meta, jsonld=jsonld)


# --------------------------------------------------------------------------- #
#  Sample courses (the interactive portfolio)
# --------------------------------------------------------------------------- #
@app.get("/samples", response_class=HTMLResponse)
def samples(request: Request, db: Session = Depends(get_session)):
    courses = db.exec(select(SampleCourse).order_by(SampleCourse.id)).all()
    course_cards = [
        {"course": course, "preview": seed.get_sample_extras(course.slug).get("preview", {})}
        for course in courses
    ]
    meta, jsonld = seo.samples_seo(request)
    return page(request, "samples.html", course_cards=course_cards,
                active="Sample Courses", meta=meta, jsonld=jsonld)


@app.get("/samples/{slug}", response_class=HTMLResponse)
def sample_detail(request: Request, slug: str, db: Session = Depends(get_session)):
    course = db.exec(select(SampleCourse).where(SampleCourse.slug == slug)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Sample not found")
    questions = db.exec(
        select(QuizQuestion)
        .where(QuizQuestion.course_id == course.id)
        .order_by(QuizQuestion.order)
    ).all()
    extras = seed.get_sample_extras(course.slug)
    course_locales = build_course_locales(course, extras, questions)
    meta, jsonld = seo.sample_detail_seo(request, course)
    return page(request, "sample_detail.html",
                course=course, questions=questions, course_locales=course_locales,
                total=len(course_locales["en"]["questions"]), active="Sample Courses",
                meta=meta, jsonld=jsonld)


@app.post("/samples/{slug}/answer/{qid}", response_class=HTMLResponse)
def answer_question(
    request: Request, slug: str, qid: int,
    choice: int = Form(0), choices: str = Form("[]"), text_answer: str = Form(""),
    locale: str = Form("en"), db: Session = Depends(get_session),
):
    """
    Backend scoring for a single knowledge check question.
    HTMX posts the chosen option(s)/text and we return a result fragment.
    This is the core interactive pattern: the answer key never reaches
    the browser until the learner has answered.
    """
    q = db.get(QuizQuestion, qid)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    course = db.exec(select(SampleCourse).where(SampleCourse.slug == slug)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Sample not found")
    questions = db.exec(
        select(QuizQuestion)
        .where(QuizQuestion.course_id == course.id)
        .order_by(QuizQuestion.order)
    ).all()
    extras = seed.get_sample_extras(course.slug)
    locale_bundle = get_locale_bundle(course, extras, questions, locale)
    localized_question = locale_bundle["questions"][q.order]
    qtype = localized_question["qtype"]

    correct_set = submitted_set = None
    accepted_display = None
    if qtype == "multi_select":
        submitted_set = set(json.loads(choices))
        correct_set = bitmask_to_set(q.correct)
        correct = submitted_set == correct_set
    elif qtype == "fill_blank":
        def normalize(s: str) -> str:
            return " ".join(s.strip().lower().split())
        accepted_list = localized_question["accepted"].split("|")
        accepted_display = " / ".join(accepted_list)
        correct = normalize(text_answer) in {normalize(a) for a in accepted_list}
    else:
        correct = (choice == q.correct)

    return page(request, "partials/quiz_result.html",
                q=q, choice=choice, correct=correct, qtype=qtype,
                correct_set=sorted(correct_set) if correct_set is not None else None,
                submitted_set=sorted(submitted_set) if submitted_set is not None else None,
                text_answer=text_answer, accepted_display=accepted_display,
                localized_question=localized_question, ui=locale_bundle["ui"],
                target_id=f"q-{locale}-{q.id}")


@app.post("/samples/{slug}/match", response_class=HTMLResponse)
def answer_matching(
    request: Request, slug: str,
    pairing: str = Form(...), locale: str = Form("en"), db: Session = Depends(get_session),
):
    """Scores the drag-and-drop matching activity. The correct pairing is
    derived server-side from the canonical (untranslated) extras data, never
    from a translated copy, and is never sent to the browser before this call."""
    course = db.exec(select(SampleCourse).where(SampleCourse.slug == slug)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Sample not found")
    questions = db.exec(
        select(QuizQuestion)
        .where(QuizQuestion.course_id == course.id)
        .order_by(QuizQuestion.order)
    ).all()
    extras = seed.get_sample_extras(course.slug)
    locale_bundle = get_locale_bundle(course, extras, questions, locale)
    localized_question = next(q for q in locale_bundle["questions"] if q["id"] == "matching-0")

    matching = extras["matching_activity"]
    pairs = matching["pairs"]
    shuffled_right = seeded_shuffle(range(len(pairs)), f"match-{course.slug}")
    correct_pairing = {str(i): shuffled_right.index(i) for i in range(len(pairs))}
    submitted = {str(k): v for k, v in json.loads(pairing).items()}
    correct = submitted == correct_pairing
    pairs_feedback = [
        {
            "left": pairs[i]["left"],
            "right": pairs[i]["right"],
            "ok": submitted.get(str(i)) == correct_pairing[str(i)],
        }
        for i in range(len(pairs))
    ]

    return page(request, "partials/quiz_result.html",
                qtype="matching", correct=correct, pairs_feedback=pairs_feedback,
                localized_question=localized_question, ui=locale_bundle["ui"],
                target_id=f"q-{locale}-matching-0")


@app.post("/samples/{slug}/sequence", response_class=HTMLResponse)
def answer_sequencing(
    request: Request, slug: str,
    order: str = Form(...), locale: str = Form("en"), db: Session = Depends(get_session),
):
    """Scores the drag-to-reorder sequencing activity against the canonical
    (untranslated) step order in extras."""
    course = db.exec(select(SampleCourse).where(SampleCourse.slug == slug)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Sample not found")
    questions = db.exec(
        select(QuizQuestion)
        .where(QuizQuestion.course_id == course.id)
        .order_by(QuizQuestion.order)
    ).all()
    extras = seed.get_sample_extras(course.slug)
    locale_bundle = get_locale_bundle(course, extras, questions, locale)
    localized_question = next(q for q in locale_bundle["questions"] if q["id"] == "sequencing-0")

    sequencing = extras["sequencing_activity"]
    submitted_order = json.loads(order)
    correct = submitted_order == sequencing["steps"]

    return page(request, "partials/quiz_result.html",
                qtype="sequencing", correct=correct,
                submitted_order=submitted_order, correct_order=sequencing["steps"],
                localized_question=localized_question, ui=locale_bundle["ui"],
                target_id=f"q-{locale}-sequencing-0")


# --------------------------------------------------------------------------- #
#  Blog ("Paseka's Thoughts")
# --------------------------------------------------------------------------- #
@app.get("/blog", response_class=HTMLResponse)
def blog(request: Request, db: Session = Depends(get_session)):
    posts = published_posts(db)
    meta, jsonld = seo.blog_seo(request)
    return page(request, "blog.html", posts=posts, active="Articles", meta=meta, jsonld=jsonld,
                site_base=seo.base_url(request))


@app.get("/blog/{slug}", response_class=HTMLResponse)
def blog_post(request: Request, slug: str, db: Session = Depends(get_session)):
    post = db.exec(select(BlogPost).where(BlogPost.slug == slug)).first()
    if not post or not post.is_published:
        raise HTTPException(status_code=404, detail="Post not found")
    paragraphs = [p.strip() for p in post.body.split("\n\n") if p.strip()]
    meta, jsonld = seo.blog_post_seo(request, post)
    return page(request, "blog_post.html", post=post, paragraphs=paragraphs,
                active="Articles", meta=meta, jsonld=jsonld)


# --------------------------------------------------------------------------- #
#  Contact
# --------------------------------------------------------------------------- #
@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    meta, jsonld = seo.contact_seo(request)
    return page(request, "contact.html", active="Contact", submitted=False,
                meta=meta, jsonld=jsonld)


@app.post("/contact", response_class=HTMLResponse)
def contact_submit(
    request: Request,
    name: str = Form(...), email: str = Form(...),
    country: str = Form(""), time_zone: str = Form(""),
    organisation: str = Form(""), service: str = Form(""),
    message: str = Form(""), preferred_date: str = Form(""),
    db: Session = Depends(get_session),
):
    lead = Lead(name=name, email=email, country=country, time_zone=time_zone,
                organisation=organisation,
                service=service, message=message, preferred_date=preferred_date)
    db.add(lead)
    db.commit()
    try:
        send_contact_email(name, email, country, time_zone, organisation,
                           service, message, preferred_date)
    except Exception:
        logger.exception("Failed to send contact submission email.")
    if request.headers.get("HX-Request") == "true":
        return page(request, "partials/contact_success.html", name=name)
    meta, jsonld = seo.contact_seo(request)
    return page(request, "contact.html", active="Contact", submitted=True, name=name,
                meta=meta, jsonld=jsonld)
