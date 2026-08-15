from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_db
from app.subscription.user._user_repository import UserRepository


class UserPlanResult:
    """Data transfer object for user plan query results."""

    def __init__(self, plan_id: int, plan_name: str, max_number_accounts: int):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.max_number_accounts = max_number_accounts


class QueryUserPlan:
    """Service for querying a user's active subscription plan."""

    user_repository: UserRepository

    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def execute(self, email: str) -> UserPlanResult | None:
        """Execute the query to find the user's active plan."""
        result = await self.user_repository.get_by_email(email)
        if not result:
            return None

        plan_active = result.get_active_plan()
        if not plan_active:
            return None

        return UserPlanResult(
            plan_id=result.id,  # type: ignore
            plan_name=result.name,  # type: ignore
            max_number_accounts=result.max_number_accounts,
        )


async def get_query_user_plan(
    db: AsyncSession = Depends(get_db),
) -> QueryUserPlan | None:
    """FastAPI dependency that provides a QueryUserPlan service instance."""
    return QueryUserPlan(db)
