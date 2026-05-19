
#app/ai/contracts/retrieval.py

from pydantic import BaseModel

class RetrievedSchema(BaseModel):
    """schema chunk comes from qdrant"""

    table_name: str
    schema_text: str
    score: float