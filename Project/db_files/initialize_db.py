import os
import sqlite3

DB_PATH = "database.db"
SCHEMA_PATH = "sql/LetsIngles.sql"

def initialize_database():
    # Check if database file exists
    if not os.path.exists(DB_PATH):
        print("Creating database and tables...")
        conn = sqlite3.connect(DB_PATH)
        with open(SCHEMA_PATH, "r") as schema_file:
            schema_sql = schema_file.read()
            conn.executescript(schema_sql)
        conn.close()
        print("Database initialized.")
    else:
        print("Database already exists. No action taken.")

if __name__ == "__main__":
    initialize_database()