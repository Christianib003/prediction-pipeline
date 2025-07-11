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
    cursor = db.cursor()

    # Check if plant and disease exist
    if not cursor.execute("SELECT 1 FROM Plants WHERE plant_id = ?", (image.plant_id,)).fetchone():
        raise HTTPException(status_code=400, detail=f"Plant with ID {image.plant_id} not found.")
    if not cursor.execute("SELECT 1 FROM Diseases WHERE disease_id = ?", (image.disease_id,)).fetchone():
        raise HTTPException(status_code=400, detail=f"Disease with ID {image.disease_id} not found.")

    cursor.execute("""
        INSERT INTO ImageMetadata (filename, image_path, date_added, plant_id, disease_id)
        VALUES (?, ?, datetime('now'), ?, ?)
    """, (image.filename, image.image_path, image.plant_id, image.disease_id))
    db.commit()

    image_id = cursor.lastrowid
    return read_image(image_id=image_id, db=db)


@router.get("/images/", response_model=List[models.ImageOut])
def read_images(skip: int = 0, limit: int = 10, db: sqlite3.Connection = Depends(get_db)):
    """
    Retrieve a list of images with their metadata.
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
        ORDER BY im.image_id
        LIMIT ? OFFSET ?
    """
    cursor.execute(query, (limit, skip))
    images = cursor.fetchall()
    # Convert each row in the list to a dictionary
    return [dict(row) for row in images]


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
    cursor = db.cursor()

    # Check if image exists
    existing = cursor.execute("SELECT * FROM ImageMetadata WHERE image_id = ?", (image_id,)).fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Image not found.")

    update_fields = []
    update_values = []

    if image.filename is not None:
        update_fields.append("filename = ?")
        update_values.append(image.filename)
    if image.image_path is not None:
        update_fields.append("image_path = ?")
        update_values.append(image.image_path)
    if image.plant_id is not None:
        if not cursor.execute("SELECT 1 FROM Plants WHERE plant_id = ?", (image.plant_id,)).fetchone():
            raise HTTPException(status_code=400, detail=f"Plant with ID {image.plant_id} not found.")
        update_fields.append("plant_id = ?")
        update_values.append(image.plant_id)
    if image.disease_id is not None:
        if not cursor.execute("SELECT 1 FROM Diseases WHERE disease_id = ?", (image.disease_id,)).fetchone():
            raise HTTPException(status_code=400, detail=f"Disease with ID {image.disease_id} not found.")
        update_fields.append("disease_id = ?")
        update_values.append(image.disease_id)

    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields provided to update.")

    update_values.append(image_id)
    query = f"UPDATE ImageMetadata SET {', '.join(update_fields)} WHERE image_id = ?"
    cursor.execute(query, tuple(update_values))
    db.commit()

    return read_image(image_id=image_id, db=db)



@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(image_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    if not cursor.execute("SELECT 1 FROM ImageMetadata WHERE image_id = ?", (image_id,)).fetchone():
        raise HTTPException(status_code=404, detail="Image not found.")

    cursor.execute("DELETE FROM ImageMetadata WHERE image_id = ?", (image_id,))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)