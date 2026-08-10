import os
from collections.abc import Generator

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()

_engine: Engine | None = None
_session_local: sessionmaker | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is required")

        _engine = create_engine(database_url)

    return _engine


def get_session_local() -> sessionmaker:
    global _session_local
    if _session_local is None:
        _session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return _session_local


def get_db() -> Generator[Session, None, None]:
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()


def init_database():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS authentication"))
        conn.commit()


def create_tables():
    from app.authentication._user import (
        _User,  # noqa: F401 - import required for SQLAlchemy model discovery
    )

    engine = get_engine()
    Base.metadata.create_all(bind=engine)
