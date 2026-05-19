# tests/unit/test_formatter.py

import pytest
from unittest.mock import patch
from app.ai.formatter.response_formatter import ResponseFormatter

class TestResponseFormatter:

    def setup_method(self):
        self.formatter = ResponseFormatter()


    @patch("app.ai.formatter.response_formatter.gemini_client")
    def test_format_with_data(self, mock_llm):
        mock_llm.generate.return_value = "2 orders found for user."

        result = self.formatter.format(
            raw_data=[{"id": 1, "quantity": 2}],
            sql_query="SELECT * FROM orders;",
            intent="Get orders",
        )

        assert result.success is True
        assert result.sql_query == "SELECT * FROM orders;"

    def test_format_empty_data(self):
        result = self.formatter.format(
            raw_data=[],
            sql_query="SELECT * FROM users;",
            intent="Get users",
        )

        assert result.success is True
        assert result.raw_data == []


    def test_format_error(self):
        result = self.formatter.format_error("MySQL connection failed")

        assert result.success is False
        assert result.error == "MySQL connection failed"
        assert result.answer is not None