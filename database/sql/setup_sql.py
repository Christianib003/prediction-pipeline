import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def execute_sql_from_file(cursor, filepath):
    """Reads and executes a SQL file."""
    with open(filepath, 'r') as f:
        cursor.execute(f.read())
    print(f"Successfully executed script: {filepath}")

conn = None
try:
    print("Connecting to the database...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("Connection successful.")

    execute_sql_from_file(cursor, 'database/schema.sql')
    execute_sql_from_file(cursor, 'database/advanced.sql')

    conn.commit()
    print("All changes have been committed.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if conn is not None:
        conn.close()
        print("Database connection closed.")