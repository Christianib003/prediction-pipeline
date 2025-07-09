from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared base model for common fields
class ImageBase(BaseModel):
    filename: str
    image_path: str

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
        from_attributes = True

# Model for updating an image record (input, all fields optional)
class ImageUpdate(BaseModel):
    filename: Optional[str] = None
    image_path: Optional[str] = None
    plant_id: Optional[int] = None
    disease_id: Optional[int] = None