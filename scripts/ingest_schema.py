# scripts/ingest_schema.py

import sys
sys.path.append(".")

from app.services.rag.embedder import schema_embedder
from app.infrastructure.vector_store.qdrant_client import qdrant_store

if __name__ == "__main__":
    print("Schema ingestion start...")
    schema_embedder.embed_all_schemas()
    
    # Verify karo kitne points store hue
    count = qdrant_store.count()
    print(f"Qdrant mein total points: {count}")
    print("Done!")