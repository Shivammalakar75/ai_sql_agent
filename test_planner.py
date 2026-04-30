# test_planner.py  (root mein)

from app.services.rag.retriever import schema_retriever
from app.services.planner.llm_planner import llm_planner

query = "user 101 ka order chahiye"

schemas = schema_retriever.retrieve(query)
result = llm_planner.plan(query, schemas)

print("Intent  :", result.intent)
print("Entities:", result.entities)
print("Tables  :", result.tables_needed)
print("SQL     :", result.sql_query)






# # test_planner.py mein temporarily yeh use karo

# from app.services.rag.retriever import schema_retriever
# from app.shared.models.domain import ParsedIntent

# query = "user 101 ka order chahiye"
# schemas = schema_retriever.retrieve(query)

# # Mock intent — Gemini ki jagah hardcode karo abhi
# mock_result = ParsedIntent(
#     intent="Get all orders for user 101",
#     entities={"user_id": 101},
#     tables_needed=["users", "orders"],
#     raw_response="mocked",
#     sql_query="SELECT o.id, o.product_id, o.quantity FROM orders o WHERE o.user_id = 101;"
# )

# print("Intent  :", mock_result.intent)
# print("Entities:", mock_result.entities)
# print("Tables  :", mock_result.tables_needed)
# print("SQL     :", mock_result.sql_query)