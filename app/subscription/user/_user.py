from sqlalchemy import Column, Integer, String

from app.infra.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "subscription"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
