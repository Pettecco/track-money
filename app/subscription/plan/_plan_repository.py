from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_db
from app.subscription.plan._plan import Plan


class PlanRepository:
    """Repository for querying subscription plans."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, plan_id: int) -> Plan | None:
        """Retrieve a plan by its database identifier."""
        result = await self.db.execute(select(Plan).filter(Plan.id == plan_id))
        return result.scalar_one_or_none()


async def get_plan_repository(
    db: AsyncSession = Depends(get_db),
) -> PlanRepository:
    """FastAPI dependency that provides a PlanRepository instance."""
    return PlanRepository(db)
