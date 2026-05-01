# app/api/schemas/crud_schemas.py

from pydantic import BaseModel
from typing import Optional


# ─── User ───────────────────────────────────────
class UserCreate(BaseModel):
    id: int
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


# ─── Product ────────────────────────────────────
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


# ─── Order ──────────────────────────────────────
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