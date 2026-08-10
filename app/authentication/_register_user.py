from typing import Annotated

from fastapi.params import Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.authentication._user import _User
from app.authentication.user_repository import UserRepository, get_user_repository


class UserCreate(BaseModel):
    email: str
    name: str
    password: str


def register_user(
    body: UserCreate,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    """Create a new user."""

    if user_repository.get_by_email(body.email):
        return JSONResponse(
            status_code=400, content={"detail": "Email already registered"}
        )

    user = _User(name=body.name, email=body.email, password=body.password)

    user_repository.create(user)

    return JSONResponse(
        status_code=201, content=None, headers={"Location": f"/users/{user.id}"}
    )
