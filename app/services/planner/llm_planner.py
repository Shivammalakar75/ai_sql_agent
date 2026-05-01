# app/services/planner/llm_planner.py

import json
from app.infrastructure.llm.gemini_client import gemini_client
from app.shared.models.domain import RetrievedSchema, ParsedIntent
from app.shared.logger import get_logger
from app.shared.exceptions import IntentParsingError

logger = get_logger(__name__)


class LLMPlanner:

    def _build_prompt(self, user_query: str, schemas: list[RetrievedSchema]) -> str:
        schema_text = "\n\n".join([s.schema_text for s in schemas])

        return f"""You are an expert MySQL query generator.

    Database Schemas:
    {schema_text}

    User Query: "{user_query}"

    Important rules:
    - Only write simple, correct MySQL SELECT queries
    - Do NOT use correlated subqueries
    - For comparisons use straightforward JOINs and HAVING clauses
    - Always use table aliases
    - Column names must exactly match the schema
    - End query with semicolon

    Respond ONLY with a valid JSON object:
    {{
        "intent": "short description in english",
        "entities": {{"key": "value"}},
        "tables_needed": ["table1", "table2"],
        "sql_query": "SELECT ... FROM ... WHERE ...;"
    }}

    No markdown, no explanation, only JSON.
    """

    def plan(self, user_query: str, schemas: list[RetrievedSchema]) -> ParsedIntent:
        prompt = self._build_prompt(user_query, schemas)
        logger.info(f"Sending query to Gemini: '{user_query}'")

        raw_response = gemini_client.generate(prompt)
        logger.debug(f"Gemini raw response: {raw_response}")

        try:
            # Markdown code block hata do agar aaya toh
            clean = raw_response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            clean = clean.strip()

            data = json.loads(clean)

            return ParsedIntent(
                intent=data["intent"],
                entities=data.get("entities", {}),
                tables_needed=data.get("tables_needed", []),
                raw_response=raw_response,
                sql_query=data.get("sql_query", ""),
            )

        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse Gemini response: {e}")
            raise IntentParsingError(
                message="Gemini ka response parse nahi hua",
                details={"raw": raw_response, "error": str(e)},
            )


# Singleton
llm_planner = LLMPlanner()