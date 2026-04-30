# test_db.py  (root mein banao, baad mein delete kar dena)

from app.infrastructure.db.mysql_client import mysql_client

# Test 1: Simple query
rows = mysql_client.execute_query("SELECT * FROM users")
print("Users:", rows)

# Test 2: Schema fetch
schema = mysql_client.get_table_schema("orders")
print("Orders schema:", schema)