from sqlalchemy import Column, Integer, String

from app.authentication._password import get_password_hash
from app.domain_exception import DomainException
from app.infra.database import Base


class _User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "authentication"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    email = Column(String(128), unique=True, index=True)
    hashed_password = Column(String(512))

    def __init__(self, name: str, email: str, password: str):
        DomainException.validate(
            name is not None and len(name) <= 128,
            "Name must be at most 128 characters long.",
        )
        self.name = name

        DomainException.validate(
            email is not None and len(email) <= 128,
            "Email must be at most 128 characters long.",
        )
        self.email = email

        DomainException.validate(
            password is not None and len(password) >= 8,
            "Password must be a non-empty string with a minimum length of 8 characters.",
        )
        self.hashed_password = get_password_hash(password)
