"""
Database models (SQLModel = SQLAlchemy + Pydantic in one).

Tables:
  SampleCourse   one previewable mock course
  QuizQuestion   a knowledge check question belonging to a sample course
  BlogPost       a "Paseka's Thoughts" article
  Lead           a contact form submission
  PageView       one page visit, with time-on-page filled in when known
  FormAttempt    one contact form POST, successful or blocked (e.g. by captcha)
  LoginAttempt   one /admin/login POST, used for rate limiting and lockout

The interactive backend lives around QuizQuestion: the browser posts answers,
FastAPI scores them server side, and returns a result fragment via HTMX.
"""
from typing import Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field


class SampleCourse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    title: str
    tool: str                 # Articulate Rise, Articulate 365, H5P
    framework: str            # Bloom's, ADDIE, SAM, Gagne
    audience: str
    duration: str
    summary: str
    outcomes: str             # newline separated, one outcome per line
    body: Optional[str] = None  # course content sections, double-newline separated
    accent: str = "teal"      # badge colour key for the UI


class QuizQuestion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="samplecourse.id", index=True)
    order: int = 0
    prompt: str
    # Options and the correct index are stored simply for a minimal setup.
    option_a: str
    option_b: str
    option_c: str
    correct: int              # 0, 1, or 2
    explanation: str          # shown after answering


class BlogPost(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    title: str
    category: str
    excerpt: str
    body: str                 # simple paragraphs separated by blank lines
    published: date = Field(default_factory=date.today)
    is_published: bool = Field(default=False)  # draft until set True from /admin
    image_path: Optional[str] = None       # cover image, under /static/uploads/blog/
    attachment_path: Optional[str] = None  # downloadable PDF/document, same folder
    attachment_name: Optional[str] = None  # original filename, shown on the download link


class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    country: str = ""
    time_zone: str = ""
    organisation: str = ""
    service: str = ""
    message: str = ""
    preferred_date: str = ""
    created: datetime = Field(default_factory=datetime.utcnow)


class PageView(SQLModel, table=True):
    """One page visit. Reported by app/static/js/analytics.js: a pageview is
    logged on load, then duration_seconds is filled in via a second,
    best-effort beacon when the visitor leaves or switches away from the
    tab. Anonymous: visitor_id is a random id a browser keeps in
    localStorage, not tied to any personal data."""
    id: Optional[int] = Field(default=None, primary_key=True)
    path: str = Field(index=True)
    visitor_id: str = Field(default="", index=True)
    referrer: str = ""
    user_agent: str = ""
    duration_seconds: Optional[float] = None
    created: datetime = Field(default_factory=datetime.utcnow, index=True)


class FormAttempt(SQLModel, table=True):
    """One POST to /contact, whether or not it went through. Lets the
    analytics dashboard show a submit funnel (attempts vs completed leads)
    and surface how much traffic the captcha is blocking."""
    id: Optional[int] = Field(default=None, primary_key=True)
    success: bool = Field(default=False, index=True)
    reason: str = ""  # "ok", "captcha_failed"
    lead_id: Optional[int] = Field(default=None, foreign_key="lead.id")
    created: datetime = Field(default_factory=datetime.utcnow, index=True)


class LoginAttempt(SQLModel, table=True):
    """One POST to /admin/login. Powers a sliding-window rate limit: an IP
    with too many recent failures is locked out until enough of them age
    out of the window. See admin.py's login_lockout_remaining()."""
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: str = Field(index=True)
    success: bool = Field(default=False)
    created: datetime = Field(default_factory=datetime.utcnow, index=True)
