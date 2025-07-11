import sqlite3
import os
from dotenv import load_dotenv
from pathlib import Path
# Load environment variables from the .env file
load_dotenv()

# Get the database path from the environment variable
# BASE_DIR is the folder where db_connector.py is located
BASE_DIR = Path(__file__).resolve().parent

# Corrected path: go up two folders and into the "database" folder
DATABASE_PATH = (BASE_DIR / os.getenv("DATABASE_PATH")).resolve()

def get_db_connection():
    """
    Establishes a connection to the SQLite database
    using the path from environment variables.
    """
    if not DATABASE_PATH:
        raise ValueError("DATABASE_PATH not set in environment variables")
    print(f"Connecting to database at {DATABASE_PATH}")    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn