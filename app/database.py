"""
SQLite database setup. The database file (paseka.db) is created next to the
project on first run. No database server needed.
"""
from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine

DB_PATH = Path(__file__).resolve().parent.parent / "paseka.db"
ENGINE = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=False,
    connect_args={"check_same_thread": False},
)


def init_db() -> None:
    """Create tables if they do not exist yet."""
    SQLModel.metadata.create_all(ENGINE)


def get_session() -> Session:
    """FastAPI dependency that yields a database session."""
    with Session(ENGINE) as session:
        yield session
