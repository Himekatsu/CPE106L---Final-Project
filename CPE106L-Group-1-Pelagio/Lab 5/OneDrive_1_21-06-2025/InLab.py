import sqlite3

# Connect to the database
conn = sqlite3.connect("chinook.db")
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT FirstName, LastName FROM employees;")

# Fetch and print results
results = cursor.fetchall()
for row in results:
    print(row)

# Clean up
conn.close()

