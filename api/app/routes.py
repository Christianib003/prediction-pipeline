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
    pass

@router.get("/images/{image_id}", response_model=models.ImageOut)
def read_image(image_id: int, db: sqlite3.Connection = Depends(get_db)):
    pass

@router.put("/images/{image_id}", response_model=models.ImageOut)
def update_image(image_id: int, image: models.ImageUpdate, db: sqlite3.Connection = Depends(get_db)):
    pass

@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(image_id: int, db: sqlite3.Connection = Depends(get_db)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)