
#app/ai/contracts/__init__.py

from app.ai.contracts.query import QueryInput
from app.ai.contracts.retrieval import RetrievedSchema
from app.ai.contracts.intent import ParsedIntent
from app.ai.contracts.sql import GeneratedSQL
from app.ai.contracts.pipeline import PipelineResult


__all__ = [
    "QueryInput",
    "RetrievedSchema",
    "ParsedIntent",
    "GeneratedSQL",
    "PipelineResult",
]