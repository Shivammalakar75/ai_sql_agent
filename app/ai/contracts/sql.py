
#app/ai/contracts/sql.py

from typing import Optional
from pydantic import BaseModel

class GeneratedSQL(BaseModel):
    """SQL builder output"""

    query: str
    is_valid: bool
    validation_message: Optional[str] = None