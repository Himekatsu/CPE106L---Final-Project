import os
import sqlite3

DB_PATH = "database.db"
SCHEMA_PATH = "sql/LetsIngles.sql"

def db_connection():
    """Returns a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def initialize_database():
    # Check if database file exists
    if not os.path.exists(DB_PATH):
        print("Creating database and tables...")
        conn = db_connection()
        with open(SCHEMA_PATH, "r") as schema_file:
            schema_sql = schema_file.read()
            conn.executescript(schema_sql)
        conn.close()
        print("Database initialized.")
    else:
        print("Database already exists. No action taken.")