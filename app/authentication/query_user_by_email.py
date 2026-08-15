from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication._user_repository import UserRepository
from app.infra.database import get_db


class UserByEmailResult:
    """Data transfer object for user query results."""

    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email


class QueryUserByEmail:
    """Service for querying authentication users by email address."""

    user_repository: UserRepository

    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def execute(self, email: str) -> UserByEmailResult | None:
        """Execute the query to find a user by email."""
        user = self.user_repository.get_by_email(email)
        if not user:
            return None
        return UserByEmailResult(id=user.id, name=user.name, email=user.email)  # type: ignore


def get_query_user_by_email(
    db: AsyncSession = Depends(get_db),
) -> QueryUserByEmail | None:
    """FastAPI dependency that provides a QueryUserByEmail service instance."""
    return QueryUserByEmail(db)
