import sqlite3

def list_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [table[0] for table in tables]

def display_table(cursor, table_name):
    print(f"\n--- {table_name} ---")
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [info[1] for info in cursor.fetchall()]
    print(" | ".join(columns))
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    for row in rows:
        print(" | ".join(str(item) for item in row))

def main():
    db_file = "CATdata.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    tables = list_tables(cursor)
    if not tables:
        print("No tables found in the database.")
        return

    print("Tables found in CATdata.db:")
    for table in tables:
        print(f"- {table}")

    for table in tables:
        display_table(cursor, table)

    conn.close()

if __name__ == "__main__":
    main()