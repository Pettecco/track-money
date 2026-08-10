from sqlalchemy import Column, Integer, String

from app.authentication._password import get_password_hash, verify_password
from app.domain_exception import DomainException
from app.infra.database import Base


class _User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "authentication"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True, index=True)
    hashed_password = Column(String(512), nullable=False)

    def __init__(self, name: str, email: str, password: str):
        DomainException.validate(
            bool(name) and len(name) <= 128,
            "Name is required and must be at most 128 characters long.",
        )
        self.name = name

        DomainException.validate(
            bool(email) and len(email) <= 128,
            "Email is required and must be at most 128 characters long.",
        )
        self.email = email

        DomainException.validate(
            bool(password) and len(password) >= 8,
            "Password must be a non-empty string with a minimum length of 8 characters.",
        )
        self.hashed_password = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify the provided password against the stored hashed password"""
        return verify_password(password, str(self.hashed_password))
