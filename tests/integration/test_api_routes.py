
# tests/integration/test_api_routes.py

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthRoute:

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestQueryRoute:

    @patch("app.api.routes.query.orchestrator")
    def test_query_success(self, mock_orch):
        from app.ai.contracts import PipelineResult

        mock_orch.run.return_value = PipelineResult(
            success=True,
            answer="Shivam has 2 orders.",
            sql_query="SELECT * FROM orders WHERE user_id=101;",
            raw_data=[{"id": 1, "quantity": 2}],
        )

        response = client.post(
            "/query",
            json={"query": "show shivam orders"}
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "answer" in response.json()

    @patch("app.api.routes.query.orchestrator")
    def test_query_failure(self, mock_orch):
        from app.ai.contracts import PipelineResult

        mock_orch.run.return_value = PipelineResult(
            success=False,
            answer="Something went wrong",
            error="Table not found",
        )

        response = client.post(
            "/query",
            json={"query": "anything"}
        )

        assert response.status_code == 200
        assert response.json()["success"] is False

    def test_query_missing_field(self):
        response = client.post("/query", json={})
        assert response.status_code == 422

    def test_query_empty_string(self):
        response = client.post("/query", json={"query": ""})
        assert response.status_code == 200


class TestCRUDRoutes:

    @patch("app.modules.user.user_router.mysql_client")
    @patch("app.modules.user.user_router.user_service")
    def test_get_all_users(self, mock_service, mock_db):
        mock_db.get_session.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_db.get_session.return_value.__exit__  = MagicMock(return_value=False)
        mock_service.get_all.return_value = []

        response = client.get("/user/users")
        assert response.status_code == 200

    @patch("app.modules.user.user_router.mysql_client")
    @patch("app.modules.user.user_router.user_service")
    def test_get_user_not_found(self, mock_service, mock_db):
        mock_db.get_session.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_db.get_session.return_value.__exit__  = MagicMock(return_value=False)
        mock_service.get_by_id.return_value = None

        response = client.get("/user/users/9999")
        assert response.status_code == 404