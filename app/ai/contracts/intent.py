
#app/ai/contracts/intent.py

from pydantic import BaseModel

class ParsedIntent(BaseModel):
    """LLM planner output"""

    intent: str
    entities: dict
    tables_needed: list[str]
    raw_response: str
    sql_query: str = ""