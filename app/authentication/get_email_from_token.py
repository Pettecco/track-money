import os

from fastapi import Depends, HTTPException
from jose import JWTError, jwt

from app.authentication._auth import oauth2_scheme


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
