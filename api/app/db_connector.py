import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the database path from the environment variable
DATABASE_PATH = os.getenv("DATABASE_PATH")

def get_db_connection():
    """
    Establishes a connection to the SQLite database
    using the path from environment variables.
    """
    if not DATABASE_PATH:
        raise ValueError("DATABASE_PATH not set in environment variables")
        
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn