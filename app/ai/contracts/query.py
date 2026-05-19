

#app/ai/contracts/query.py

from pydantic import BaseModel

class QueryInput(BaseModel):
    """User raw input"""

    text: str