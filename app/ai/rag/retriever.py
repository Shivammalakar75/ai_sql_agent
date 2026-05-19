# app/ai/rag/retriever.py

from sentence_transformers import SentenceTransformer
from app.infrastructure.vector_store.qdrant_client import qdrant_store
from app.core.config import settings
from app.ai.contracts import RetrievedSchema
from app.core.logger import get_logger

logger = get_logger(__name__)


class SchemaRetriever:

    def __init__(self):
        self._model = SentenceTransformer(settings.embedding_model)
        logger.info("Schema retriever ready")

    def retrieve(self, query: str, top_k: int = settings.top_k_schemas) -> list[RetrievedSchema]:
        """
        Find similar matches to the user's query in Qdrent.

        Example:
            query = "orders details of user 101"
            returns = [orders schema, users schema]
        """
        logger.info(f"Retrieving schemas for: '{query}'")

        query_vector = self._model.encode(query).tolist()

        results = qdrant_store.search(
            query_vector=query_vector,
            top_k=top_k,
        )

        schemas = [
            RetrievedSchema(
                table_name=r["table_name"],
                schema_text=r["schema_text"],
                score=r["score"],
            )
            for r in results
        ]

        logger.info(f"Found {len(schemas)} relevant schemas: "
                    f"{[s.table_name for s in schemas]}")

        return schemas


# Singleton
schema_retriever = SchemaRetriever()