from pydantic import BaseModel
from datetime import datetime
from .base import BaseSchema

class TourBase(BaseModel):
    title: str
    description: str | None = None
    location: str
    duration_days: int
    max_participants: int
    price: int

class TourCreate(TourBase):
    pass

class TourUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    duration_days: int | None = None
    max_participants: int | None = None
    price: int | None = None
    is_active: bool | None = None

class Tour(TourBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
