from typing import Annotated

from fastapi.params import Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.authentication._user import User
from app.authentication._user_repository import UserRepository, get_user_repository


class UserCreate(BaseModel):
    """Request body schema for user registration."""

    email: str
    name: str
    password: str


async def register_user(
    body: UserCreate,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    """Register a new user in the system."""

    if await user_repository.get_by_email(body.email):
        return JSONResponse(
            status_code=400, content={"detail": "Email already registered"}
        )

    user = User(name=body.name, email=body.email, password=body.password)

    await user_repository.create(user)

    return JSONResponse(
        status_code=201, content=None, headers={"Location": f"/users/{user.id}"}
    )
