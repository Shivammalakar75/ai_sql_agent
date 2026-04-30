# app/api/middleware/error_handler.py

from fastapi import Request
from fastapi.responses import JSONResponse
from app.shared.logger import get_logger

logger = get_logger(__name__)


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "answer": "Internal server error",
            "error": str(exc),
        },
    )