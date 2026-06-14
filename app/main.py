"""
FastAPI application.

Run from the project root with:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000
"""
from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path
import smtplib
from email.message import EmailMessage

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.database import init_db, get_session
from app.models import SampleCourse, QuizQuestion, BlogPost, Lead
from app.data import content as C
from app import seed

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
logger = logging.getLogger(__name__)

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
        "quiz_intro": "Answer each question. Scoring happens on the server, the answer key is never sent to your browser early.",
        "correct": "Correct",
        "not_quite": "Not quite",
        "why": "Why:",
        "score_prefix": "You scored",
        "score_suffix": "",
        "score_text": "This is the kind of immediate, low stakes feedback that keeps learners moving. Every sample course is built the same way: outcomes first, then practice, then feedback.",
        "contact_cta": "Request a course like this",
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
    load_local_env()
    init_db()
    seed.run()          # seeds only if empty
    yield


app = FastAPI(title="Paseka eLearning", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Make site wide content available to every template.
templates.env.globals.update(SITE=C.SITE, NAV=C.NAV, NAV_SLUGS=C.NAV_SLUGS, SERVICE_MENU=C.SERVICE_MENU)


def page(request: Request, template: str, **ctx) -> HTMLResponse:
    return templates.TemplateResponse(request, template, ctx)


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


def build_localized_questions(questions: list[QuizQuestion], translation: dict | None = None) -> list[dict]:
    translated = translation or {}
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
            "explanation": data.get("explanation", q.explanation),
            "correct": q.correct,
        })
    return localized


def build_course_locales(course: SampleCourse, extras: dict, questions: list[QuizQuestion]) -> dict[str, dict]:
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
            "questions": build_localized_questions(questions),
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
            "questions": build_localized_questions(questions, data),
            "ui": UI_LABELS.get(code, UI_LABELS["en"]),
        }
    return locales


def get_locale_bundle(course: SampleCourse, extras: dict, questions: list[QuizQuestion], locale: str) -> dict:
    locales = build_course_locales(course, extras, questions)
    return locales.get(locale, locales["en"])


# --------------------------------------------------------------------------- #
#  Static content pages
# --------------------------------------------------------------------------- #
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return page(request, "index.html",
                value_props=C.VALUE_PROPS, who=C.WHO_I_HELP, active="Home")


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return page(request, "about.html", cv=C.CV, active="About")


@app.get("/services/{slug}", response_class=HTMLResponse)
def service_page(request: Request, slug: str):
    data = C.SERVICE_PAGES.get(slug)
    if not data:
        raise HTTPException(status_code=404, detail="Service not found")
    return page(request, "service_page.html",
                data=data, slug=slug, frameworks=C.FRAMEWORKS,
                active="Services")


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
    return page(request, "samples.html", course_cards=course_cards, active="Sample Courses")


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
    return page(request, "sample_detail.html",
                course=course, questions=questions, course_locales=course_locales,
                total=len(questions), active="Sample Courses")


@app.post("/samples/{slug}/answer/{qid}", response_class=HTMLResponse)
def answer_question(
    request: Request, slug: str, qid: int,
    choice: int = Form(...), locale: str = Form("en"), db: Session = Depends(get_session),
):
    """
    Backend scoring for a single knowledge check question.
    HTMX posts the chosen option and we return a result fragment.
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
    correct = (choice == q.correct)
    return page(request, "partials/quiz_result.html",
                q=q, choice=choice, correct=correct,
                localized_question=localized_question, ui=locale_bundle["ui"],
                target_id=f"q-{locale}-{q.id}")


# --------------------------------------------------------------------------- #
#  Blog ("Paseka's Thoughts")
# --------------------------------------------------------------------------- #
@app.get("/blog", response_class=HTMLResponse)
def blog(request: Request, db: Session = Depends(get_session)):
    posts = db.exec(select(BlogPost).order_by(BlogPost.published.desc())).all()
    return page(request, "blog.html", posts=posts, active="Blog")


@app.get("/blog/{slug}", response_class=HTMLResponse)
def blog_post(request: Request, slug: str, db: Session = Depends(get_session)):
    post = db.exec(select(BlogPost).where(BlogPost.slug == slug)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    paragraphs = [p.strip() for p in post.body.split("\n\n") if p.strip()]
    return page(request, "blog_post.html", post=post, paragraphs=paragraphs, active="Blog")


# --------------------------------------------------------------------------- #
#  Contact
# --------------------------------------------------------------------------- #
@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return page(request, "contact.html", active="Contact", submitted=False)


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
    return page(request, "contact.html", active="Contact", submitted=True, name=name)
