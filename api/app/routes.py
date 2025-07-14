from fastapi import APIRouter, Depends, status
from typing import List
import psycopg2
from pymongo.database import Database
from . import models
from .db_connectors import get_postgres_db, get_mongo_db

router = APIRouter()

@router.get("/images/{image_id}")
def get_image_by_id(image_id: int, db: psycopg2.extensions.connection = Depends(get_postgres_db)):
    pass

@router.post("/predictions/", status_code=status.HTTP_201_CREATED)
def log_prediction(log_data: models.PredictionLogCreate, db: Database = Depends(get_mongo_db)):
    pass
