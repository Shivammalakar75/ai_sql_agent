# tests/unit/test_validator.py

import pytest
from app.ai.workflows.orchestrator import Orchestrator
from app.core.exceptions import SQLValidationError

orchestrator = Orchestrator()


class TestSQLValidator:

    def test_valid_select(self):
        orchestrator._validate_sql("SELECT * FROM users;")

    def test_valid_select_with_join(self):
        orchestrator._validate_sql(
            "SELECT u.name, o.quantity FROM users u "
            "JOIN orders o ON u.id = o.user_id;"
        )

    def test_valid_select_uppercase(self):
        orchestrator._validate_sql("SELECT id FROM users;")

    def test_invalid_drop(self):
        with pytest.raises(SQLValidationError):
            orchestrator._validate_sql("DROP TABLE users;")

    def test_invalid_delete(self):
        with pytest.raises(SQLValidationError):
            orchestrator._validate_sql("DELETE FROM users;")

    def test_invalid_update(self):
        with pytest.raises(SQLValidationError):
            orchestrator._validate_sql("UPDATE users SET name='x';")

    def test_invalid_insert(self):
        with pytest.raises(SQLValidationError):
            orchestrator._validate_sql("INSERT INTO users VALUES (1,'x','x');")

    def test_invalid_empty(self):
        with pytest.raises(SQLValidationError):
            orchestrator._validate_sql("")

    def test_invalid_truncate(self):
        with pytest.raises(SQLValidationError):
            orchestrator._validate_sql("TRUNCATE TABLE users;")