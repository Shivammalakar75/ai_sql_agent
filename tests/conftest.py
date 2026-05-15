# tests/conftest.py

import sys
import pytest
from unittest.mock import MagicMock, patch


# ── Block Qdrant connection before any import ──────────────────
mock_qdrant_client = MagicMock()
mock_qdrant_instance = MagicMock()
mock_qdrant_instance.get_collections.return_value.collections = []
mock_qdrant_instance.search.return_value = []
mock_qdrant_instance.upsert.return_value = None
mock_qdrant_instance.count.return_value.count = 0
mock_qdrant_client.return_value = mock_qdrant_instance

# Inject fake QdrantClient before app imports it
sys.modules["qdrant_client"] = MagicMock(QdrantClient=mock_qdrant_client)
sys.modules["qdrant_client.models"] = MagicMock(
    Distance=MagicMock(COSINE="cosine"),
    VectorParams=MagicMock(),
    PointStruct=MagicMock(),
)

# Block Sentence Transformer connection
mock_st = MagicMock()
mock_st_instance = MagicMock()
mock_st_instance.encode.return_value = [0.1] * 384
mock_st.return_value = mock_st_instance
sys.modules["sentence_transformers"] = MagicMock(
    SentenceTransformer=mock_st
)
# ──────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)


@pytest.fixture
def mock_mysql():
    mock = MagicMock()
    mock.execute_query.return_value = [
        {"id": 1, "name": "Shivam", "email": "shivam@gmail.com"},
        {"id": 2, "name": "Rahul",  "email": "rahul@gmail.com"},
    ]
    mock.get_table_schema.return_value = [
        {"Field": "id",    "Type": "int"},
        {"Field": "name",  "Type": "varchar(30)"},
        {"Field": "email", "Type": "varchar(100)"},
    ]
    return mock


@pytest.fixture
def mock_groq():
    mock = MagicMock()
    mock.generate.return_value = (
        '{"intent": "Get all users", '
        '"entities": {}, '
        '"tables_needed": ["users"], '
        '"sql_query": "SELECT * FROM users;"}'
    )
    return mock


@pytest.fixture
def sample_schemas():
    from app.shared.models.domain import RetrievedSchema
    return [
        RetrievedSchema(
            table_name="users",
            schema_text="Table: users\nColumns:\n  - id (int)\n  - name (varchar(30))\n  - email (varchar(100))",
            score=0.85
        ),
        RetrievedSchema(
            table_name="orders",
            schema_text="Table: orders\nColumns:\n  - id (int)\n  - user_id (int)\n  - product_id (int)\n  - quantity (int)",
            score=0.75
        ),
    ]


@pytest.fixture
def sample_raw_data():
    return [
        {"id": 1, "user_id": 101, "product_id": 1, "quantity": 2},
        {"id": 2, "user_id": 101, "product_id": 2, "quantity": 1},
    ]