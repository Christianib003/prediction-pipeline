from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Image Models for PostgreSQL

class ImageBase(BaseModel):
    filename: str
    image_path: str

class ImageCreate(ImageBase):
    plant_name: str
    disease_name: str

class ImageUpdate(BaseModel):
    filename: Optional[str] = None
    image_path: Optional[str] = None
    plant_id: Optional[int] = None 
    disease_id: Optional[int] = None

class ImageOut(ImageBase):
    image_id: int
    date_added: datetime
    plant_name: str
    disease_name: str

    class Config:
        from_attributes = True

# Prediction Log Model for MongoDB

class PredictionLogCreate(BaseModel):
    sql_image_id: int
    predicted_class_name: str
    confidence_score: float