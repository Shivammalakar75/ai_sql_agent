
# app/modules/product/product_schema

from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    id: int
    name: str
    price: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int

    model_config = {"from_attributes": True}
