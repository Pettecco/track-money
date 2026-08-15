import datetime
import os

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.authentication._user import User


def generate_jwt_token(user: User) -> str:
    """Generate a JWT access token for the given user."""
    expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")

    if not expire_minutes:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES environment variable is not set.")
    if not secret_key:
        raise ValueError("SECRET_KEY environment variable is not set.")
    if not algorithm:
        raise ValueError("ALGORITHM environment variable is not set.")

    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=int(expire_minutes)
    )

    payload = {"sub": user.email, "name": user.name, "exp": expire}
    token = jwt.encode(payload, secret_key, algorithm)

    return token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
