import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# SQL command to truncate all tables and reset ID counters
TRUNCATE_COMMAND = """
TRUNCATE TABLE 
    image_metadata, 
    plants, 
    diseases,
    image_metadata_audit
RESTART IDENTITY CASCADE;
"""

conn = None
try:
    # Connect to the PostgreSQL database
    print("Connecting to the PostgreSQL database...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("Connection successful.")

    # Execute the truncate command
    print("Clearing all tables...")
    cursor.execute(TRUNCATE_COMMAND)
    
    # Commit the transaction to make the changes permanent
    conn.commit()
    print("All tables cleared successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
    # Rollback changes if anything went wrong
    if conn:
        conn.rollback()
finally:
    # Always close the connection
    if conn is not None:
        conn.close()
        print("Database connection closed.")