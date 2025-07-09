from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared base model for common fields
class ImageBase(BaseModel):
    filename: str
    storage_path: str

# Model for creating a new image record (input)
class ImageCreate(ImageBase):
    plant_id: int
    disease_id: int

# Model for reading an image record from the DB (output)
class ImageOut(ImageBase):
    image_id: int
    date_added: datetime
    plant_name: str
    disease_name: str

    class Config:
        from_attributes = True # Formerly orm_mode = True