
# app/modules/user/user_schema.py

from pydantic import BaseModel
from typing import Optional

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
