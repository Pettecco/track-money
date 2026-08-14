from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.domain_exception import DomainException
from app.infra.database import Base
from app.subscription.plan._plan import Plan
from app.subscription.user._user_plan import UserPlan


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "subscription"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)

    user_plans = relationship("UserPlan", back_populates="user")

    def __init__(self, name: str, email: str):
        DomainException.validate(
            bool(name) and len(name) <= 128,
            "Name must be a non-empty string with a maximum length of 128 characters.",
        )
        self.name = name

        DomainException.validate(
            bool(email) and len(email) <= 128,
            "Name must be a non-empty string with a maximum length of 128 characters.",
        )
        self.email = email

    def add_plan(self, plan: Plan, credit_card: str | None):
        DomainException.validate(
            plan is not None, "Plan must be provided to add to the user"
        )

        if not bool(plan.is_free):
            DomainException.validate(
                bool(credit_card), "Credit card must be provided for non-free plans"
            )

        self._deactive_plans()
        user_plan = UserPlan(plan=plan, active=True, credit_card=credit_card)
        self.user_plans.append(user_plan)

    def _deactive_plans(self):
        for user_plan in self.user_plans:
            user_plan.active = False
