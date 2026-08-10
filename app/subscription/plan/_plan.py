import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from app.domain_exception import DomainException
from app.infra.database import Base


class Plan(Base):
    __tablename__ = "plans"
    __table_args__ = {"schema": "subscription"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(24), unique=True, index=True, nullable=False)
    max_number_accounts = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    is_free = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, name: str, max_number_accounts: int, price: float):
        DomainException.validate(
            bool(name) and len(name) <= 24,
            "Name is required and must be at most 24 characters long",
        )
        self.name = name

        DomainException.validate(
            max_number_accounts >= 0,
            "Max number banking must be a non-negative integer",
        )
        self.max_number_accounts = max_number_accounts

        DomainException.validate(
            price >= 0.0,
            "Price must be a non-negative number",
        )
        self.price = price

        self.is_free = False
        if price == 0:
            self.is_free = True
        self.created_at = datetime.datetime.now(datetime.UTC)
