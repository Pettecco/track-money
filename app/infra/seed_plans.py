import asyncio
import datetime

from dotenv import load_dotenv

from app.infra.database import create_tables, get_engine

load_dotenv()
from app.subscription.plan._plan import (
    Plan,  # ruff: ignore[module-import-not-at-top-of-file]
)


async def seed_plans():
    await create_tables()

    engine = get_engine()
    async with engine.begin() as conn:
        existing = await conn.execute(Plan.__table__.select())
        if existing.rowcount > 0:
            print("Plans already seeded")
            return

        now = datetime.datetime.utcnow()
        await conn.execute(
            Plan.__table__.insert().values([
                {
                    "name": "Free Plan",
                    "max_number_accounts": 1,
                    "price": 0.0,
                    "is_free": True,
                    "created_at": now,
                },
                {
                    "name": "Basic Plan",
                    "max_number_accounts": 5,
                    "price": 9.99,
                    "is_free": False,
                    "created_at": now,
                },
                {
                    "name": "Premium Plan",
                    "max_number_accounts": 15,
                    "price": 19.99,
                    "is_free": False,
                    "created_at": now,
                },
            ])
        )
        print("Plans seeded successfully")


if __name__ == "__main__":
    asyncio.run(seed_plans())
