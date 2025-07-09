from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .app import db_connector

# Create the FastAPI app instance
app = FastAPI(
    title="Plant Disease API",
    description="API for accessing plant disease dataset metadata.",
    version="1.0.0"
)

# Dependency to get a DB session
def get_db():
    db = db_connector.get_db_connection()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Plant Disease API!"}

@app.get("/test-db")
def test_database_connection(db: Session = Depends(get_db)):
    """
    An endpoint to test the database connection by fetching one plant.
    """
    try:
        cursor = db.cursor()
        cursor.execute("SELECT plant_name FROM Plants LIMIT 1")
        plant = cursor.fetchone()
        if plant:
            return {"status": "Database connection successful", "first_plant": plant['plant_name']}
        return {"status": "Database connection successful", "message": "No plants found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")