import os
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

_engine: AsyncEngine | None = None
_session_local: async_sessionmaker | None = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is required")

        _engine = create_async_engine(database_url)

    return _engine


def get_session_local() -> async_sessionmaker:
    global _session_local
    if _session_local is None:
        _session_local = async_sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine(), class_=AsyncSession
        )
    return _session_local


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = get_session_local()()
    try:
        yield db
    finally:
        await db.close()


async def init_database():
    engine = get_engine()
    async with engine.connect() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS authentication"))
        await conn.commit()


async def create_tables():
    from app.authentication._user import (
        User,  # noqa: F401 - import required for SQLAlchemy model discovery
    )

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
