from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from .base import BaseSchema, TimestampMixin

class TourBase(BaseSchema):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    location: str = Field(..., min_length=2, max_length=200)
    duration_days: int = Field(..., gt=0, le=365)
    max_participants: int = Field(..., gt=0, le=1000)
    price: int = Field(..., gt=0)  # Price in cents
    is_active: bool = True

class TourCreate(TourBase):
    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip().title()
    
    @validator('location')
    def validate_location(cls, v):
        if not v.strip():
            raise ValueError('Location cannot be empty')
        return v.strip().title()

class TourUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = Field(None, min_length=2, max_length=200)
    duration_days: Optional[int] = Field(None, gt=0, le=365)
    max_participants: Optional[int] = Field(None, gt=0, le=1000)
    price: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None
    
    @validator('title')
    def validate_title(cls, v):
        if v and not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip().title() if v else v
    
    @validator('location')
    def validate_location(cls, v):
        if v and not v.strip():
            raise ValueError('Location cannot be empty')
        return v.strip().title() if v else v

class Tour(TourBase, TimestampMixin):
    id: int
    created_at: datetime

class TourStats(BaseModel):
    total: int = Field(..., description="Total number of tours")
    active: int = Field(..., description="Number of active tours")
    inactive: int = Field(..., description="Number of inactive tours")
    participants: int = Field(..., description="Total participants in active tours")
    
    class Config:
        schema_extra = {
            "example": {
                "total": 15,
                "active": 12,
                "inactive": 3,
                "participants": 245
            }
        }
