# app/api/routes/query.py

from fastapi import APIRouter
from app.api.schemas.request import QueryRequest
from app.api.schemas.response import QueryResponse
from app.ai.workflows.orchestrator import orchestrator
from app.ai.contracts import QueryInput
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    logger.info(f"Request recieve: '{request.query}'")

    result = orchestrator.run(
        QueryInput(text=request.query)
    )

    return QueryResponse(
        success=result.success,
        answer=result.answer,
        sql_query=result.sql_query,
        raw_data=result.raw_data,
        error=result.error,
    )