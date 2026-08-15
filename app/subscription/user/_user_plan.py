from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infra.database import Base
from app.subscription.plan._plan import Plan


class UserPlan(Base):
    """SQLAlchemy model representing the relationship between a user and their subscription plan."""

    __tablename__ = "user_plans"
    __table_args__ = {"schema": "subscription"}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("subscription.users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey(Plan.id), nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    credit_card = Column(String(24), nullable=True)  # Only for didatic methods
    created_at = Column(DateTime, nullable=False)

    user = relationship("app.subscription.user._user.User", back_populates="user_plans")
    plan = relationship(Plan)

    def __init__(
        self,
        plan: Plan,
        active: bool,
        credit_card: str | None,
    ):
        """Initialize a UserPlan with the given plan, active status, and optional credit card."""
        self.plan = plan
        self.active = active
        self.credit_card = credit_card
        self.created_at = datetime.now(UTC)
