
# test_planner.py 

from app.services.rag.retriever import schema_retriever
from app.shared.models.domain import ParsedIntent

query = "user 101 ka order chahiye"
schemas = schema_retriever.retrieve(query)

# Mock intent — Gemini ki jagah hardcode karo abhi
mock_result = ParsedIntent(
    intent="Get all orders for user 101",
    entities={"user_id": 101},
    tables_needed=["users", "orders"],
    raw_response="mocked",
    sql_query="SELECT o.id, o.product_id, o.quantity FROM orders o WHERE o.user_id = 101;"
)

print("Intent  :", mock_result.intent)
print("Entities:", mock_result.entities)
print("Tables  :", mock_result.tables_needed)
print("SQL     :", mock_result.sql_query)