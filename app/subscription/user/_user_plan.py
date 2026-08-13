from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.domain_exception import DomainException
from app.infra.database import Base
from app.subscription.plan._plan import Plan
from app.subscription.user._user import User


class UserPlan(Base):
    __tablename__ = "user_plans"
    __table_args__ = {"schema": "subscription"}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    plan_id = Column(Integer, ForeignKey(Plan.id), nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    credit_card = Column(String(24), nullable=True)  # Only for didatic methods
    created_at = Column(DateTime, nullable=False)

    user = relationship(User, back_populates="user_plans")
    plan = relationship(Plan, back_populates="user_plans")

    def __init__(
        self,
        user_id: int,
        plan_id: int,
        active: bool,
        credit_card: str | None,
    ):
        DomainException.validate(user_id > 0, "User ID must be a positive integer.")
        self.user_id = user_id

        DomainException.validate(plan_id > 0, "Plan ID must be a positive integer.")
        self.plan_id = plan_id

        self.active = active
        self.credit_card = credit_card
        self.created_at = datetime.now(UTC)
