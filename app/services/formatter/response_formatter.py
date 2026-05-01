# app/services/formatter/response_formatter.py

from app.shared.models.domain import PipelineResult
from app.shared.logger import get_logger
from app.infrastructure.llm.gemini_client import gemini_client

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

        answer = self.generate_natural_answer(raw_data, intent)
        answer = answer.replace("\n", " ")

        return PipelineResult(
            success=True,
            answer=answer,
            sql_query=sql_query,
            raw_data=raw_data,
        )

    def format_error(self, error_message: str) -> PipelineResult:
        """Error hone pe standard error response banao"""
        return PipelineResult(
            success=False,
            answer=f"Kuch problem aayi: {error_message}",
            error=error_message,
        )

    def generate_natural_answer(self, raw_data, intent, user_query=None):
        from app.infrastructure.llm.gemini_client import gemini_client

        prompt = f"""
    You are an intelligent SQL assistant.

    User question:
    {user_query}

    Intent:
    {intent}

    Database result:
    {raw_data}

    RULES:
    - Answer MUST be in SAME language as user question
    - If user writes Hindi → reply Hindi
    - If English → English
    - If Hinglish → Hinglish
    - Keep answer short and readable
    - Convert data into human readable sentence
    - Do NOT return JSON or raw format
    """

        response = gemini_client.generate(prompt)
        return response

# Singleton
response_formatter = ResponseFormatter()