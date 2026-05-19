
# app/modules/order/order_schema.py

from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

class OrderUpdate(BaseModel):
    quantity: Optional[int] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    model_config = {"from_attributes": True}