from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5437/track_money_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS authentication"))
        conn.commit()


def create_tables():
    from app.authentication._user import (
        _User,  # noqa: F401 - import required for SQLAlchemy model discovery
    )

    Base.metadata.create_all(bind=engine)
