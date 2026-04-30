# app/services/formatter/response_formatter.py

from app.shared.models.domain import PipelineResult
from app.shared.logger import get_logger

logger = get_logger(__name__)


class ResponseFormatter:

    def format(
        self,
        raw_data: list[dict],
        sql_query: str,
        intent: str,
    ) -> PipelineResult:
        """
        MySQL ka raw result readable answer mein convert karo.
        """
        logger.info(f"Formatting {len(raw_data)} rows")

        if not raw_data:
            return PipelineResult(
                success=True,
                answer=" Data not found for your query.",
                sql_query=sql_query,
                raw_data=[],
            )

        answer = self._build_answer(raw_data, intent)

        return PipelineResult(
            success=True,
            answer=answer,
            sql_query=sql_query,
            raw_data=raw_data,
        )

    def _build_answer(self, rows: list[dict], intent: str) -> str:
        lines = [f"Query: {intent}", f"Total records found: {len(rows)}", ""]

        for idx, row in enumerate(rows, start=1):
            lines.append(f"Record {idx}:")
            for key, value in row.items():
                lines.append(f"  {key}: {value}")
            lines.append("")

        return "\n".join(lines)

    def format_error(self, error_message: str) -> PipelineResult:
        """Error hone pe standard error response banao"""
        return PipelineResult(
            success=False,
            answer=f"Kuch problem aayi: {error_message}",
            error=error_message,
        )


# Singleton
response_formatter = ResponseFormatter()