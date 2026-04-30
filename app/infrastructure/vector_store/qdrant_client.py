# app/infrastructure/vector_store/qdrant_client.py

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)
from app.shared.config import settings
from app.shared.constants import (
    SCHEMA_COLLECTION_NAME,
    EMBEDDING_DIM,
    TOP_K_SCHEMAS,
)
from app.shared.logger import get_logger
from app.shared.exceptions import SchemaRetrievalError

logger = get_logger(__name__)


class QdrantVectorStore:

    def __init__(self):
        self._client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )
        self._collection = SCHEMA_COLLECTION_NAME
        self._ensure_collection()
        logger.info("Qdrant client ready")

    def _ensure_collection(self):
        """
        Collection exist nahi karti toh create karo.
        Already exist karti hai toh kuch mat karo.
        """
        existing = [c.name for c in self._client.get_collections().collections]

        if self._collection not in existing:
            self._client.create_collection(
                collection_name=self._collection,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIM,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Collection '{self._collection}' created")
        else:
            logger.info(f"Collection '{self._collection}' already exists")

    def upsert(self, points: list[PointStruct]):
        """
        Schema embeddings Qdrant mein store karo.
        """
        self._client.upsert(
            collection_name=self._collection,
            points=points,
        )
        logger.info(f"{len(points)} points upserted")

    def search(self, query_vector: list[float], top_k: int = TOP_K_SCHEMAS) -> list[dict]:
        """
        Query vector se similar schemas dhundho.
        """
        try:
            results = self._client.query_points(
                collection_name=self._collection,
                query=query_vector,
                limit=top_k,
                with_payload=True,
            )
            return [
                {
                    "table_name": r.payload.get("table_name"),
                    "schema_text": r.payload.get("schema_text"),
                    "score": r.score,
                }
                for r in results.points
            ]

        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            raise SchemaRetrievalError(
                message="Schema retrieve nahi hua",
                details={"error": str(e)},
            )

    def count(self) -> int:
        """Kitne points hain collection mein"""
        result = self._client.count(collection_name=self._collection)
        return result.count


# Singleton
qdrant_store = QdrantVectorStore()