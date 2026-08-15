from decimal import Decimal

from sqlalchemy import Column, Enum, Integer, Numeric, String
from sqlalchemy.orm import composite

from app.domain_exception import DomainException
from app.infra.database import Base


class AccountStatus(Enum):
    """Enumeration for account status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    CLOSED = "closed"
    SUSPENDED = "suspended"


class User:
    """Value object representing a user associated with a bank account."""

    name: str
    email: str

    def __init__(self, name: str, email: str):
        """Initialize a User with validated name and email."""
        DomainException.validate(
            bool(name) and len(name) <= 128,
            "Name must be a non-empty string with maximum 128 characters.",
        )
        self.name = self.name

        DomainException.validate(
            bool(email) and "@" in email and len(email) <= 128,
            "Email must be a valid email address with maximum 128 characters.",
        )
        self.email = self.email

    def __composite_values__(self):
        """Required method for SQLAlchemy composite."""
        return self.name, self.email


class BankAccount(Base):
    """SQLAlchemy model representing a user's bank account."""

    __tablename__ = "bank_accounts"
    __table_args__ = {"schema": "movement"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(24), nullable=False)
    bank_name = Column(String(24), nullable=False)
    account_number = Column(String(24), nullable=False, unique=True)
    balance = Column(Numeric(precision=15), nullable=False, default=0)
    status = Column(String(20), nullable=False, default=AccountStatus.ACTIVE)
    _user_name = Column("user_name", String(128), nullable=False)
    _user_email = Column("user_email", String(128), nullable=False)
    user = composite(User, _user_name, _user_email)

    def __init__(
        self,
        name: str,
        bank_name: str,
        account_number: str,
        user: User,
        balance: Decimal = 0,  # pyright: ignore[reportArgumentType]
        status: AccountStatus = AccountStatus.ACTIVE,  # pyright: ignore[reportArgumentType]
    ):
        """Initialize a BankAccount with validated fields."""
        self.name = name
        self.bank_name = bank_name
        self.account_number = account_number
        self.user = user
        self.balance = balance
        self.status = status

        DomainException.validate(
            bool(name) and len(name) <= 24,
            "Account name must be a non-empty string with maximum 24 characters.",
        )
        DomainException.validate(
            bool(bank_name) and len(bank_name) <= 24,
            "Bank name must be a non-empty string with maximum 24 characters.",
        )
        DomainException.validate(
            bool(account_number) and len(account_number) <= 24,
            "Account number must be a non-empty string with maximum 128 characters.",
        )
        DomainException.validate(
            bool(isinstance(balance, (int, float)) and balance >= 0),
            "Balance must be a non-negative number.",
        )
