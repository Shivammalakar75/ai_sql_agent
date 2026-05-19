# app/modules/user/user_model.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String(100), nullable=False)

    orders = relationship("Order", back_populates="user")