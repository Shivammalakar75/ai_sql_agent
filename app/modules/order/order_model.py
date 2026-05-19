# app/infrastructure/db/models.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
