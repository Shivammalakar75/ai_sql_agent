# app/api/schemas/request.py

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str