from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List, Dict, Any
import psycopg2
import psycopg2.extras
from pymongo.database import Database
from . import models
from .db_connectors import get_postgres_db, get_mongo_db
from datetime import datetime

# Main Router for SQL Operations
router = APIRouter(
    prefix="/images",
    tags=["SQL Image Metadata (CRUD)"]
)


@router.get("/{image_id}", response_model=models.ImageOut)
def get_image_by_id(image_id: int, db: psycopg2.extensions.connection = Depends(get_postgres_db)):
    """Retrieve a single image's metadata by its ID."""
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
        SELECT
            im.image_id, im.filename, im.image_path, im.date_added,
            p.plant_name, d.disease_name
        FROM image_metadata im
        JOIN plants p ON im.plant_id = p.plant_id
        JOIN diseases d ON im.disease_id = d.disease_id
        WHERE im.image_id = %s;
    """
    cursor.execute(query, (image_id,))
    record = cursor.fetchone()
    if not record:
        raise HTTPException(status_code=404, detail="Image not found")
    return record

@router.get("/latest/", response_model=models.ImageOut)
def read_latest_image(db: psycopg2.extensions.connection = Depends(get_postgres_db)):
    """Retrieve the most recently added image's metadata."""
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = "SELECT im.image_id, im.filename, im.image_path, im.date_added, p.plant_name, d.disease_name FROM image_metadata im JOIN plants p ON im.plant_id = p.plant_id JOIN diseases d ON im.disease_id = d.disease_id ORDER BY im.date_added DESC LIMIT 1;"
    cursor.execute(query)
    record = cursor.fetchone()
    if not record:
        raise HTTPException(status_code=404, detail="No images found")
    return record

@router.get("/", response_model=List[models.ImageOut])
def get_all_images(skip: int = 0, limit: int = 10, db: psycopg2.extensions.connection = Depends(get_postgres_db)):
    """Retrieve a list of all images with pagination."""
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = "SELECT im.image_id, im.filename, im.image_path, im.date_added, p.plant_name, d.disease_name FROM image_metadata im JOIN plants p ON im.plant_id = p.plant_id JOIN diseases d ON im.disease_id = d.disease_id ORDER BY im.image_id LIMIT %s OFFSET %s;"
    cursor.execute(query, (limit, skip))
    records = cursor.fetchall()
    return records


@router.post("/", response_model=models.ImageOut, status_code=status.HTTP_201_CREATED)
def create_image(image: models.ImageCreate, db: psycopg2.extensions.connection = Depends(get_postgres_db)):
    """Create a new image metadata record by calling the stored procedure."""
    cursor = db.cursor()
    try:
        cursor.callproc('add_new_image', (image.filename, image.image_path, image.plant_name, image.disease_name))
        db.commit()
        cursor.execute("SELECT image_id FROM image_metadata WHERE image_path = %s", (image.image_path,))
        new_id = cursor.fetchone()[0]
        return get_image_by_id(new_id, db)
    except psycopg2.Error as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {e}")



@router.put("images/{image_id}", response_model=models.ImageOut)
def update_image(image_id: int, image_update: models.ImageUpdate, db: psycopg2.extensions.connection = Depends(get_postgres_db)):
    """Update an existing image metadata record."""
    get_image_by_id(image_id, db)
    
    update_data = image_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    set_clauses = [f"{key} = %s" for key in update_data.keys()]
    query = f"UPDATE image_metadata SET {', '.join(set_clauses)} WHERE image_id = %s"
    
    values = list(update_data.values())
    values.append(image_id)
    
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    
    return get_image_by_id(image_id, db)



@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(image_id: int, db: psycopg2.extensions.connection = Depends(get_postgres_db)):
    """Delete an image metadata record."""
    get_image_by_id(image_id, db)
    cursor = db.cursor()
    cursor.execute("DELETE FROM image_metadata WHERE image_id = %s", (image_id,))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Router for MongoDB Logging Operations
log_router = APIRouter(
    prefix="/predictions",
    tags=["MongoDB Prediction Logging"]
)

@log_router.post("/", status_code=status.HTTP_201_CREATED)
def log_prediction(log_data: models.PredictionLogCreate, db: Database = Depends(get_mongo_db)):
    """Logs prediction results into MongoDB."""
    images_collection = db.images
    # Find the document using the ID from the SQL database
    image_document = images_collection.find_one({"sql_image_id": log_data.sql_image_id})

    if not image_document:
        raise HTTPException(status_code=404, detail="Image not found in MongoDB to log prediction against.")

    prediction_entry = {
        "predicted_class_name": log_data.predicted_class_name,
        "confidence_score": log_data.confidence_score,
        "prediction_date": datetime.now()
    }
    
    images_collection.update_one(
        {"_id": image_document["_id"]},
        {"$push": {"predictions": prediction_entry}}
    )

    return {"message": "Prediction logged successfully"}