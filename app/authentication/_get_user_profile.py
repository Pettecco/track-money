from fastapi import Depends
from pydantic import BaseModel

from app.authentication._user_repository import UserRepository, get_user_repository
from app.authentication.get_email_from_token import get_email_from_token


class UserProfileReponse(BaseModel):
    """Response schema for user profile data."""

    email: str
    name: str

    class Config:
        from_attributes = True


async def get_user_profile(
    email: str = Depends(get_email_from_token),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserProfileReponse:
    """Retrieve the authenticated user's profile."""
    user = await user_repository.get_by_email(email)
    return user
