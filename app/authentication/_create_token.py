from typing import Annotated

from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.authentication._auth import generate_jwt_token
from app.authentication.user_repository import UserRepository, get_user_repository


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> TokenResponse | JSONResponse:
    """Create a JWT token for the user."""
    user = await user_repository.get_by_email(form_data.username)
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

    if not user.verify_password(form_data.password):
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

    token = generate_jwt_token(user)
    return TokenResponse(access_token=token)
