# app/infrastructure/db/mysql_client.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager
from app.shared.config import settings
from app.shared.logger import get_logger
from app.shared.exceptions import DatabaseExecutionError

logger = get_logger(__name__)


class MySQLClient:

    def __init__(self):
        url = (
            f"mysql+pymysql://{settings.mysql_user}:{settings.mysql_password}"
            f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_database}"
        )
        self._engine = create_engine(
            url,
            pool_pre_ping=True,   # connection alive hai check karo
            pool_size=5,
            max_overflow=10,
            echo=(settings.app_env == "development"),
        )
        self._Session = sessionmaker(bind=self._engine)
        logger.info("MySQL engine ready")

    @contextmanager
    def get_session(self):         
        session = self._Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def execute_query(self, sql: str) -> list[dict]:
        """
        SELECT query chalao aur rows return karo.
        SQLAlchemy 2.0 style — with statement use karo.
        """
        try:
            with self._engine.connect() as conn:
                result = conn.execute(text(sql))
                rows = result.mappings().all()
                return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Query failed: {sql} | Error: {e}")
            raise DatabaseExecutionError(
                message="MySQL query execute nahi hui",
                details={"sql": sql, "error": str(e)}
            )

    def get_table_schema(self, table_name: str) -> list[dict]:
        """
        Kisi bhi table ka schema fetch karo.
        DESCRIBE table_name use karta hai.
        """
        try:
            with self._engine.connect() as conn:
                result = conn.execute(text(f"DESCRIBE {table_name}"))
                return [dict(row._mapping) for row in result]
        except Exception as e:
            logger.error(f"Schema fetch failed for {table_name}: {e}")
            raise DatabaseExecutionError(
                message=f"{table_name} ka schema nahi mila",
                details={"table": table_name, "error": str(e)}
            )

    def dispose(self):
        """App band hone pe connection pool close karo"""
        self._engine.dispose()
        logger.info("MySQL connection pool closed")


# Singleton instance
mysql_client = MySQLClient()