from fastapi import Depends
from pydantic import BaseModel

from app.authentication._auth import get_email_from_token
from app.authentication.user_repository import UserRepository, get_user_repository


class UserProfileReponse(BaseModel):
    email: str
    name: str

    class Config:
        from_attributes = True


async def get_user_profile(
    email: str = Depends(get_email_from_token),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserProfileReponse:
    """Get the user profile based on the email extracted from the JWT token."""
    user = await user_repository.get_by_email(email)
    return user
