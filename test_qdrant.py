# test_qdrant.py

from app.infrastructure.vector_store.qdrant_client import qdrant_store

count = qdrant_store.count()
print(f"Qdrant ready! Points in collection: {count}")