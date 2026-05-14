# app/services/crud/history_service.py

from sqlalchemy.orm import Session
from app.infrastructure.db.models import QueryHistory
from app.shared.logger import get_logger

logger = get_logger(__name__)


class HistoryService:

    def save(
        self,
        session: Session,
        user_query: str,
        sql_query: str = None,
        success: bool = True,
        error: str = None,
    ) -> QueryHistory:
        record = QueryHistory(
            user_query=user_query,
            sql_query=sql_query,
            success=success,
            error=error,
        )
        session.add(record)
        session.flush()
        logger.info(f"Query history saved | success: {success}")
        return record

    def get_all(self, session: Session) -> list[QueryHistory]:
        return (
            session.query(QueryHistory)
            .order_by(QueryHistory.created_at.desc())
            .all()
        )

    def get_failed(self, session: Session) -> list[QueryHistory]:
        return (
            session.query(QueryHistory)
            .filter(QueryHistory.success == False)
            .order_by(QueryHistory.created_at.desc())
            .all()
        )

    def get_recent(self, session: Session, limit: int = 10) -> list[QueryHistory]:
        return (
            session.query(QueryHistory)
            .order_by(QueryHistory.created_at.desc())
            .limit(limit)
            .all()
        )


# Singleton
history_service = HistoryService()