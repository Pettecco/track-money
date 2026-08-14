from fastapi import Depends
from pydantic import BaseModel

from app.authentication import (
    QueryUserByEmail,
    get_email_from_token,
    get_query_user_by_email,
)
from app.subscription.plan._plan_repository import PlanRepository, get_plan_repository
from app.subscription.user._user import User
from app.subscription.user._user_repository import UserRepository, get_user_repository


class SelectPlanCreate(BaseModel):
    plan_id: int
    credit_card: str | None = None


async def select_plan(
    body: SelectPlanCreate,
    email: str = Depends(get_email_from_token),
    user_repository: UserRepository = Depends(get_user_repository),
    plan_repository: PlanRepository = Depends(get_plan_repository),
    query_user_by_email: QueryUserByEmail = Depends(get_query_user_by_email),
) -> None:
    user = user_repository.get_by_email(email)
    if not user:
        user_auth = query_user_by_email.execute(email)
        user = User(name=user_auth.name, email=email)  # type: ignore

    plan = plan_repository.get_by_id(body.plan_id)
    user.add_plan(plan, body.credit_card)
    user_repository.create(user)
