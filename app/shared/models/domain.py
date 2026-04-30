# app/shared/models/domain.py

from pydantic import BaseModel
from typing import Optional


class QueryInput(BaseModel):
    """User ka raw input"""
    text: str                        # "user 101 ka order chahiye"


class RetrievedSchema(BaseModel):
    """Qdrant se aaya schema chunk"""
    table_name: str
    schema_text: str
    score: float                     # similarity score


class ParsedIntent(BaseModel):
    """LLM planner ka output"""
    intent: str                      # "get_user_orders"
    entities: dict                   # {"user_id": 101}
    tables_needed: list[str]         # ["users", "orders"]
    raw_response: str
    sql_query: str = ""


class GeneratedSQL(BaseModel):
    """SQL builder ka output"""
    query: str
    is_valid: bool
    validation_message: Optional[str] = None


class PipelineResult(BaseModel):
    """Final answer jo user ko milega"""
    success: bool
    answer: str
    sql_query: Optional[str] = None
    raw_data: Optional[list] = None
    error: Optional[str] = None