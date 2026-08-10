import datetime
import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.authentication._user import _User


def generate_jwt_token(user: _User) -> str:
    """Generate a JWT token for the user."""
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


async def get_email_from_token(
    token: str = Depends(oauth2_scheme),
) -> str:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        secret_key = os.getenv("SECRET_KEY")
        algorithm = os.getenv("ALGORITHM")

        if not secret_key or not algorithm:
            raise credentials_exception

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        return str(email)
    except JWTError:
        raise credentials_exception
