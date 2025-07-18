from database_utils import initialize_database, db_connection

# Initialize database (run once; it won't overwrite existing db)
initialize_database()

# Example: Use db_connection to run a query
conn = db_connection()
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print("Tables in database:", tables)
conn.close()