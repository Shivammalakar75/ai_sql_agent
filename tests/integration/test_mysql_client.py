# tests/integration/test_mysql_client.py

import pytest
from unittest.mock import patch, MagicMock
from app.infrastructure.db.mysql_client import MySQLClient
from app.core.exceptions import DatabaseExecutionError


class TestMySQLClient:

    @patch("app.infrastructure.db.mysql_client.create_engine")
    @patch("app.infrastructure.db.mysql_client.sessionmaker")
    def setup_method(self, method, mock_session, mock_engine):
        self.client = MySQLClient()
        self.mock_engine = MagicMock()
        self.client._engine = self.mock_engine

    def test_execute_query_returns_rows(self):
        mock_conn = MagicMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = [
            {"id": 1, "name": "Shivam"},
            {"id": 2, "name": "Rahul"},
        ]
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value = mock_result
        self.mock_engine.connect.return_value = mock_conn

        rows = self.client.execute_query("SELECT * FROM users;")

        assert len(rows) == 2
        assert rows[0]["name"] == "Shivam"

    def test_execute_query_returns_empty(self):
        mock_conn = MagicMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = []
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value = mock_result
        self.mock_engine.connect.return_value = mock_conn

        rows = self.client.execute_query("SELECT * FROM users WHERE id=9999;")

        assert rows == []

    def test_execute_query_raises_on_error(self):
        mock_conn = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.side_effect = Exception("Table does not exist")
        self.mock_engine.connect.return_value = mock_conn

        with pytest.raises(DatabaseExecutionError):
            self.client.execute_query("SELECT * FROM invalid_table;")

    def test_get_table_schema_returns_columns(self):
        mock_conn = MagicMock()
        mock_row1 = MagicMock()
        mock_row1._mapping = {"Field": "id",   "Type": "int"}
        mock_row2 = MagicMock()
        mock_row2._mapping = {"Field": "name", "Type": "varchar(30)"}
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value = [mock_row1, mock_row2]
        self.mock_engine.connect.return_value = mock_conn

        schema = self.client.get_table_schema("users")

        assert len(schema) == 2
        assert schema[0]["Field"] == "id"
        assert schema[1]["Field"] == "name"

    def test_get_table_schema_raises_on_error(self):
        mock_conn = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.side_effect = Exception("Table not found")
        self.mock_engine.connect.return_value = mock_conn

        with pytest.raises(DatabaseExecutionError):
            self.client.get_table_schema("invalid_table")

    def test_get_session_commits_on_success(self):
        mock_session = MagicMock()
        self.client._Session = MagicMock(return_value=mock_session)

        with self.client.get_session() as session:
            pass

        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    def test_get_session_rollback_on_error(self):
        mock_session = MagicMock()
        self.client._Session = MagicMock(return_value=mock_session)

        with pytest.raises(Exception):
            with self.client.get_session() as session:
                raise Exception("Something went wrong")

        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()

    def test_dispose_closes_engine(self):
        self.client.dispose()
        self.mock_engine.dispose.assert_called_once()