# app/shared/constants.py

# Qdrant
SCHEMA_COLLECTION_NAME = "nl_sql_schema"
EMBEDDING_DIM = 384
TOP_K_SCHEMAS = 3
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# LLM  ← yahan sirf yeh line badli
LLM_MODEL = "llama-3.3-70b-versatile"   
LLM_MAX_TOKENS = 1024
LLM_TEMPERATURE = 0.0

# SQL Safety
SQL_ALLOWED_STATEMENTS = ["SELECT"]
SQL_MAX_ROWS = 100

# Tables
DB_TABLES = ["users", "orders", "products"]