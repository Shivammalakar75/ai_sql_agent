# app/services/rag/embedder.py

from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct
from app.infrastructure.vector_store.qdrant_client import qdrant_store
from app.infrastructure.db.mysql_client import mysql_client
from app.shared.constants import EMBEDDING_MODEL, DB_TABLES
from app.shared.logger import get_logger

logger = get_logger(__name__)


class SchemaEmbedder:

    def __init__(self):
        self._model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info(f"Embedding model loaded: {EMBEDDING_MODEL}")

    def _build_schema_text(self, table_name: str) -> str:
        """
        MySQL se table ka schema fetch karo aur
        readable text mein convert karo.

        Example output:
        Table: orders
        Columns:
          - id (int)
          - user_id (int)
          - product_id (int)
          - quantity (int)
        """
        columns = mysql_client.get_table_schema(table_name)

        lines = [f"Table: {table_name}", "Columns:"]
        for col in columns:
            lines.append(f"  - {col['Field']} ({col['Type']})")

        return "\n".join(lines)

    def embed_all_schemas(self):
        """
        Sabhi tables ka schema embed karo aur Qdrant mein store karo.
        """
        points = []

        for idx, table_name in enumerate(DB_TABLES):
            schema_text = self._build_schema_text(table_name)
            logger.info(f"Embedding schema for: {table_name}")

            vector = self._model.encode(schema_text).tolist()

            points.append(
                PointStruct(
                    id=idx,
                    vector=vector,
                    payload={
                        "table_name": table_name,
                        "schema_text": schema_text,
                    },
                )
            )

        qdrant_store.upsert(points)
        logger.info(f"Done! {len(points)} schemas stored in Qdrant")


# Singleton
schema_embedder = SchemaEmbedder()