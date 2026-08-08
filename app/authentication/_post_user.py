from typing import Annotated

from fastapi.params import Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.authentication._user import _User
from app.infra.database import get_db


class UserCreate(BaseModel):
    email: str
    name: str
    password: str


def post_user(body: UserCreate, db: Annotated[Session, Depends(get_db)]):
    """Create a new user."""

    user = _User(name=body.name, email=body.email, password=body.password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return JSONResponse(
        status_code=201, content=None, headers={"Location": f"/users/{user.id}"}
    )
