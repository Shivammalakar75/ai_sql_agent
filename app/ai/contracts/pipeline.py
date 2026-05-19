
#app/ai/contracts/pipeline.py

from typing import Any, Optional
from pydantic import BaseModel

class PipelineResult(BaseModel):
    """Final answer sent to user"""

    success: bool
    answer: Any
    sql_query: Optional[str] = None
    raw_data: Optional[list] = None
    error: Optional[str] = None