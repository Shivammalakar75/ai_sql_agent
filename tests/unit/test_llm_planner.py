import pytest
from unittest.mock import patch
from app.services.planner.llm_planner import LLMPlanner
from app.shared.exceptions import IntentParsingError


class TestLLMPlanner:

    def setup_method(self):
        self.planner = LLMPlanner()

    @patch("app.services.planner.llm_planner.gemini_client")
    def test_plan_valid_response(self, mock_llm, sample_schemas):
        mock_llm.generate.return_value = (
            '{"intent": "Get all users", '
            '"entities": {}, '
            '"tables_needed": ["users"], '
            '"sql_query": "SELECT * FROM users;"}'
        )

        result = self.planner.plan("show all users", sample_schemas)

        assert result.intent == "Get all users"
        assert result.sql_query == "SELECT * FROM users;"
        assert "users" in result.tables_needed

    @patch("app.services.planner.llm_planner.gemini_client")
    def test_plan_with_markdown(self, mock_llm, sample_schemas):
        mock_llm.generate.return_value = (
            "```json\n"
            '{"intent": "Get users", "entities": {}, '
            '"tables_needed": ["users"], "sql_query": "SELECT * FROM users;"}'
            "\n```"
        )

        result = self.planner.plan("show users", sample_schemas)
        assert result.sql_query == "SELECT * FROM users;"

    @patch("app.services.planner.llm_planner.gemini_client")
    def test_plan_invalid_json(self, mock_llm, sample_schemas):
        mock_llm.generate.return_value = "This is not valid JSON"

        with pytest.raises(IntentParsingError):
            self.planner.plan("anything", sample_schemas)

    @patch("app.services.planner.llm_planner.gemini_client")
    def test_plan_prompt_contains_schema(self, mock_llm, sample_schemas):
        mock_llm.generate.return_value = (
            '{"intent": "x", "entities": {}, '
            '"tables_needed": ["users"], "sql_query": "SELECT * FROM users;"}'
        )

        self.planner.plan("test query", sample_schemas)

        call_args = mock_llm.generate.call_args[0][0]
        assert "users" in call_args
        assert "orders" in call_args