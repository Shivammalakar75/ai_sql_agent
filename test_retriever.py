# test_retriever.py  (root mein)

from app.services.rag.retriever import schema_retriever

results = schema_retriever.retrieve("user 101 ka order chahiye")

for r in results:
    print(f"\nTable: {r.table_name} | Score: {r.score:.3f}")
    print(r.schema_text)