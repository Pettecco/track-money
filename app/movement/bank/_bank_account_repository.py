from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_db
from app.movement.bank._bank_account import BankAccount


class BankAccountRepository:
    """Repository for creating and querying bank accounts."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, bank_account: BankAccount):
        """Persist a new bank account to the database."""
        self.db.add(bank_account)
        await self.db.commit()
        await self.db.refresh(bank_account)

    async def get_all_by_user(self, user_email: str) -> list[BankAccount]:
        """Retrieve all bank accounts belonging to a specific user."""
        result = await self.db.execute(
            select(BankAccount).filter(BankAccount._user_email == user_email)
        )
        return list(result.scalars().all())


async def get_bank_account_repository(
    db: AsyncSession = Depends(get_db),
) -> BankAccountRepository:
    """FastAPI dependency that provides a BankAccountRepository instance."""
    return BankAccountRepository(db)
