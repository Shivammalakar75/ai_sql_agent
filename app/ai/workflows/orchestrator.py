
# app/ai/workflows/orchestrator.py

from app.ai.rag.retriever import schema_retriever
from app.ai.planner.llm_planner import llm_planner
from app.infrastructure.db.mysql_client import mysql_client
from app.ai.formatter.response_formatter import response_formatter
from app.ai.contracts import QueryInput, PipelineResult
from app.core.config import settings
from app.core.logger import get_logger
from app.core.exceptions import SQLValidationError

logger = get_logger(__name__)


class Orchestrator:

    def run(self, query_input: QueryInput) -> PipelineResult:
        """
        whole pipeline runs here:
        1. RAG -> search relevant schemas
        2. LLM Planner -> build intent + SQL
        3. Validate -> is SQL safe?
        4. Execute -> run on MySQL
        5. Format -> built readable answer 
        """
        user_query = query_input.text
        logger.info(f"Pipeline start | query: '{user_query}'")

        try:
            # Step 1 — RAG
            schemas = schema_retriever.retrieve(user_query)
            if not schemas:
                return response_formatter.format_error(
                    "Relevant schema not found"
                )

            # Step 2 — LLM Planner
            parsed = llm_planner.plan(user_query, schemas)
            logger.info(f"Intent: {parsed.intent}")
            logger.info(f"SQL: {parsed.sql_query}")

            # Step 3 — Validate
            self._validate_sql(parsed.sql_query)

            # Step 4 — Execute
            raw_data = mysql_client.execute_query(parsed.sql_query)
            logger.info(f"Query returned {len(raw_data)} rows")

            # Step 5 — Format
            result = response_formatter.format(
                raw_data=raw_data,
                sql_query=parsed.sql_query,
                intent=parsed.intent,
            )

            logger.info("Pipeline complete!")
            return result

        except SQLValidationError as e:
            logger.error(f"SQL validation failed: {e.message}")
            return response_formatter.format_error(e.message)

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return response_formatter.format_error(str(e))

    def _validate_sql(self, sql: str):
        """Only SELECT allow"""
        sql_upper = sql.strip().upper()
        allowed = [s.upper() for s in settings.sql_allowed_statements]

        if not any(sql_upper.startswith(s) for s in allowed):
            raise SQLValidationError(
                message=f"Only {settings.sql_allowed_statements} allowed",
                details={"sql": sql},
            )


# Singleton
orchestrator = Orchestrator()