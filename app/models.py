"""
Database models (SQLModel = SQLAlchemy + Pydantic in one).

Tables:
  SampleCourse   one previewable mock course
  QuizQuestion   a knowledge check question belonging to a sample course
  BlogPost       a "Paseka's Thoughts" article
  Lead           a contact form submission

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
