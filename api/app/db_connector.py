import sqlite3
import os

# Define the path to the database file
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'plant_disease_dataset.db')

def get_db_connection():
    """
    Establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    # This allows you to access columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row
    return conn