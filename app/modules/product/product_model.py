# app/modules/product/product_model.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)

    orders = relationship("Order", back_populates="product")
