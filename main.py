# main.py

from fastapi import FastAPI
from app.api.routes import query, health
from app.api.middleware.error_handler import global_exception_handler
from app.core.logger import get_logger
# from app.api.routes.crud import router as crud_router
from app.modules import crud_router

logger = get_logger(__name__)

app = FastAPI(
    title="NL to SQL Agent",
    description="Create SQL queries using natural language",
    version="1.0.0",
)

# Middleware
app.add_exception_handler(Exception, global_exception_handler)

# Routes
app.include_router(health.router, tags=["Health"])
app.include_router(query.router, tags=["Query"])
app.include_router(crud_router) 
logger.info("App ready!")

# run -> docker run -p 6333:6333 qdrant/qdrant
# PYTHONPATH=. uvicorn main:app --reload --port 8000