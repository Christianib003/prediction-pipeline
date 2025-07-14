import os
import psycopg2
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("DATABASE_URL")
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

def get_postgres_db():
    """Dependency to get a PostgreSQL database connection."""
    conn = None
    try:
        conn = psycopg2.connect(POSTGRES_URL)
        yield conn
    finally:
        if conn is not None:
            conn.close()

def get_mongo_db():
    """Dependency to get a MongoDB database object."""
    client = None
    try:
        client = MongoClient(MONGO_URL)
        db = client[MONGO_DB_NAME]
        yield db
    finally:
        if client is not None:
            client.close()