from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_db
from app.subscription.user._user import User


class UserRepository:
    """Repository for creating and querying subscription users."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User):
        """Create a new user in the database."""
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address."""
        result = await self.db.execute(select(User).filter_by(email=email))
        return result.scalar_one_or_none()


async def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    """FastAPI dependency that provides a UserRepository instance."""
    return UserRepository(db)
