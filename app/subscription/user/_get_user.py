from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from app.authentication import get_email_from_token
from app.subscription.user._user_repository import UserRepository, get_user_repository


class PlanReponse(BaseModel):
    id: int
    name: str
    price: float
    active: bool
    is_free: bool

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    plans: list[PlanReponse] = []

    class Config:
        from_attributes = True


async def get_user(
    email: str = Depends(get_email_from_token),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserResponse:
    user = user_repository.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found",
        )

    plans = [
        PlanReponse(
            id=up.plan.id,
            name=up.plan.name,
            price=up.plan.price,
            active=up.plan.active,
            is_free=up.plan.is_free,
        )
        for up in user.user_plans
    ]

    return UserResponse(id=user.id, email=user.email, name=user.name, plans=plans)  # type: ignore[arg-type]
