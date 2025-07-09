from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List
import sqlite3
from . import models
from .db_connector import get_db_connection

router = APIRouter()

# Dependency to get a DB session
def get_db():
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()

@router.post("/images/", response_model=models.ImageOut)
def create_image(image: models.ImageCreate, db: sqlite3.Connection = Depends(get_db)):
    pass

@router.get("/images/", response_model=List[models.ImageOut])
def read_images(skip: int = 0, limit: int = 10, db: sqlite3.Connection = Depends(get_db)):
    pass

@router.get("/images/latest", response_model=models.ImageOut)
def read_latest_image(db: sqlite3.Connection = Depends(get_db)):
    """
    Retrieve the most recently added image's metadata.
    """
    cursor = db.cursor()
    query = """
        SELECT
            im.image_id, im.filename, im.image_path, im.date_added,
            p.plant_name,
            d.disease_name
        FROM ImageMetadata im
        JOIN Plants p ON im.plant_id = p.plant_id
        JOIN Diseases d ON im.disease_id = d.disease_id
        ORDER BY im.date_added DESC
        LIMIT 1
    """
    cursor.execute(query)
    image = cursor.fetchone()

    if image is None:
        raise HTTPException(status_code=404, detail="No images found in the database")
        
    return dict(image)

@router.get("/images/{image_id}", response_model=models.ImageOut)
def read_image(image_id: int, db: sqlite3.Connection = Depends(get_db)):
    """
    Retrieve a single image's metadata by its ID.
    """
    cursor = db.cursor()
    query = """
        SELECT
            im.image_id, im.filename, im.image_path, im.date_added,
            p.plant_name,
            d.disease_name
        FROM ImageMetadata im
        JOIN Plants p ON im.plant_id = p.plant_id
        JOIN Diseases d ON im.disease_id = d.disease_id
        WHERE im.image_id = ?
    """
    cursor.execute(query, (image_id,))
    image = cursor.fetchone()

    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return dict(image)

@router.put("/images/{image_id}", response_model=models.ImageOut)
def update_image(image_id: int, image: models.ImageUpdate, db: sqlite3.Connection = Depends(get_db)):
    pass

@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(image_id: int, db: sqlite3.Connection = Depends(get_db)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)