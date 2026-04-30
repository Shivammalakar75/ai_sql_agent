# app/core/orchestrator.py

from app.services.rag.retriever import schema_retriever
from app.services.planner.llm_planner import llm_planner
from app.infrastructure.db.mysql_client import mysql_client
from app.services.formatter.response_formatter import response_formatter
from app.shared.models.domain import QueryInput, PipelineResult
from app.shared.constants import SQL_ALLOWED_STATEMENTS
from app.shared.logger import get_logger
from app.shared.exceptions import SQLValidationError

logger = get_logger(__name__)


class Orchestrator:

    def run(self, query_input: QueryInput) -> PipelineResult:
        """
        Poora pipeline yahan chalता hai:
        1. RAG → relevant schemas dhundho
        2. LLM Planner → intent + SQL banao
        3. Validate → SQL safe hai?
        4. Execute → MySQL pe chalao
        5. Format → readable answer banao
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
        """Sirf SELECT allow hai"""
        sql_upper = sql.strip().upper()
        allowed = [s.upper() for s in SQL_ALLOWED_STATEMENTS]

        if not any(sql_upper.startswith(s) for s in allowed):
            raise SQLValidationError(
                message=f"Sirf {SQL_ALLOWED_STATEMENTS} allowed hai",
                details={"sql": sql},
            )


# Singleton
orchestrator = Orchestrator()