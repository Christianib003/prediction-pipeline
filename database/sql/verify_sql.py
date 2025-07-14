import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

conn = None
try:
    # Connect to the PostgreSQL database
    print("Connecting to the database...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("Connection successful.")

    # Query to get all table names from the 'public' schema
    list_tables_query = """
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public' ORDER BY table_name;
    """

    cursor.execute(list_tables_query)
    tables = cursor.fetchall()

    if tables:
        print("\nTables found in the database:")
        for table in tables:
            print(f"- {table[0]}")
    else:
        print("No tables found in the public schema.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Always close the connection
    if conn is not None:
        conn.close()
        print("\nDatabase connection closed.")