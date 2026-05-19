
# tests/integration/test_rag_pipeline.py

import pytest
from unittest.mock import patch, MagicMock
import numpy as np

class TestRAGPipeline:

    @patch("app.ai.rag.retriever.qdrant_store")
    @patch("app.ai.rag.retriever.SentenceTransformer")
    def test_retrieve_returns_schemas(self, mock_st, mock_qdrant):
        from app.ai.rag.retriever import SchemaRetriever

        mock_model = MagicMock()
        mock_model.encode.return_value = np.array([0.1] * 384)
        mock_st.return_value = mock_model

        mock_qdrant.search.return_value = [
            {"table_name": "users",  "schema_text": "Table: users",  "score": 0.85},
            {"table_name": "orders", "schema_text": "Table: orders", "score": 0.75},
        ]

        retriever = SchemaRetriever()
        results = retriever.retrieve("shivam orders")

        assert len(results) == 2
        assert results[0].table_name == "users"
        assert results[0].score == 0.85

    @patch("app.ai.rag.retriever.qdrant_store")
    @patch("app.ai.rag.retriever.SentenceTransformer")
    def test_retrieve_empty_result(self, mock_st, mock_qdrant):
        from app.ai.rag.retriever import SchemaRetriever

        mock_model = MagicMock()
        mock_model.encode.return_value = np.array([0.1] * 384)
        mock_st.return_value = mock_model

        mock_qdrant.search.return_value = []

        retriever = SchemaRetriever()
        results = retriever.retrieve("random query")

        assert results == []

    @patch("app.ai.rag.retriever.qdrant_store")
    @patch("app.ai.rag.retriever.SentenceTransformer")
    def test_retrieve_score_order(self, mock_st, mock_qdrant):
        from app.ai.rag.retriever import SchemaRetriever

        mock_model = MagicMock()
        mock_model.encode.return_value = np.array([0.1] * 384)
        mock_st.return_value = mock_model

        mock_qdrant.search.return_value = [
            {"table_name": "orders",   "schema_text": "Table: orders",   "score": 0.90},
            {"table_name": "users",    "schema_text": "Table: users",    "score": 0.80},
            {"table_name": "products", "schema_text": "Table: products", "score": 0.60},
        ]

        retriever = SchemaRetriever()
        results = retriever.retrieve("show orders")

        assert results[0].table_name == "orders"
        assert results[0].score > results[1].score