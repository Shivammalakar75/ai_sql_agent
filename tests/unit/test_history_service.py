import pytest
from unittest.mock import MagicMock
from app.services.crud.history_service import HistoryService


class TestHistoryService:

    def setup_method(self):
        self.service = HistoryService()

    def test_save_success(self):
        mock_session = MagicMock()

        self.service.save(
            session=mock_session,
            user_query="show shivam orders",
            sql_query="SELECT * FROM orders WHERE user_id=101;",
            success=True,
        )

        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()

    def test_save_failed_query(self):
        mock_session = MagicMock()

        self.service.save(
            session=mock_session,
            user_query="anything",
            sql_query=None,
            success=False,
            error="Table not found",
        )

        mock_session.add.assert_called_once()

    def test_get_all(self):
        mock_session = MagicMock()
        self.service.get_all(mock_session)
        mock_session.query.assert_called_once()

    def test_get_failed(self):
        mock_session = MagicMock()
        self.service.get_failed(mock_session)
        mock_session.query.assert_called_once()

    def test_get_recent(self):
        mock_session = MagicMock()
        self.service.get_recent(mock_session, limit=5)
        mock_session.query.assert_called_once()