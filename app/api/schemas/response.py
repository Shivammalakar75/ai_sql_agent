# app/api/schemas/response.py

from pydantic import BaseModel
from typing import Optional


class QueryResponse(BaseModel):
    success: bool
    answer: str
    sql_query: Optional[str] = None
    raw_data: Optional[list] = None
    error: Optional[str] = None