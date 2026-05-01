# app/api/schemas/response.py

from pydantic import BaseModel
from typing import Optional, Any

class QueryResponse(BaseModel):
    success: bool
    answer: Any
    sql_query: Optional[str] = None
    raw_data: Optional[list] = None
    error: Optional[str] = None