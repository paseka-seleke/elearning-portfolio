"""
SQLite database setup. The database file (paseka.db) is created next to the
project on first run. No database server needed.
"""
from pathlib import Path
from sqlalchemy import text
from sqlmodel import SQLModel, Session, create_engine

DB_PATH = Path(__file__).resolve().parent.parent / "paseka.db"
ENGINE = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=False,
    connect_args={"check_same_thread": False},
)


def _add_missing_columns() -> None:
    """create_all() only adds new tables, not new columns on existing tables.
    This adds any column that a model defines but an existing paseka.db
    predates, so the admin blog feature works without deleting the database."""
    with ENGINE.connect() as conn:
        existing = {row[1] for row in conn.execute(text("PRAGMA table_info(blogpost)"))}
        if not existing:
            return
        if "is_published" not in existing:
            conn.execute(text("ALTER TABLE blogpost ADD COLUMN is_published BOOLEAN DEFAULT 0"))
            # Posts that already existed before this feature were live on the
            # site, so treat them as published rather than hiding them.
            conn.execute(text("UPDATE blogpost SET is_published = 1"))
        if "image_path" not in existing:
            conn.execute(text("ALTER TABLE blogpost ADD COLUMN image_path VARCHAR"))
        if "attachment_path" not in existing:
            conn.execute(text("ALTER TABLE blogpost ADD COLUMN attachment_path VARCHAR"))
        if "attachment_name" not in existing:
            conn.execute(text("ALTER TABLE blogpost ADD COLUMN attachment_name VARCHAR"))
        conn.commit()


def init_db() -> None:
    """Create tables if they do not exist yet, and migrate existing ones."""
    SQLModel.metadata.create_all(ENGINE)
    _add_missing_columns()


def get_session() -> Session:
    """FastAPI dependency that yields a database session."""
    with Session(ENGINE) as session:
        yield session
