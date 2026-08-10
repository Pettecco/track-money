from typing import Annotated

from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication._user import User
from app.infra.database import get_db


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User):
        """Create a ew user in the database."""
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email"""
        result = await self.db.execute(select(User).filter_by(email=email))
        return result.scalar_one_or_none()


async def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    """Dependency to get a UserRepository instance."""
    return UserRepository(db)
