# test_pipeline.py  (root mein)

from app.core.orchestrator import orchestrator
from app.shared.models.domain import QueryInput

query = QueryInput(text="user 101 ka order chahiye")
result = orchestrator.run(query)

print("Success :", result.success)
print("Answer  :\n", result.answer)
print("SQL     :", result.sql_query)