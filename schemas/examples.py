"""
Example schemas showing advanced Pydantic patterns and validation
"""
from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

class TourStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class AdvancedTourSchema(BaseModel):
    """Example of advanced schema with comprehensive validation"""
    
    title: str = Field(..., min_length=3, max_length=200, description="Tour title")
    description: Optional[str] = Field(None, max_length=2000, description="Tour description")
    location: str = Field(..., min_length=2, max_length=200, description="Tour location")
    duration_days: int = Field(..., ge=1, le=365, description="Duration in days")
    max_participants: int = Field(..., ge=1, le=100, description="Maximum participants")
    price: int = Field(..., ge=0, description="Price in cents")
    start_date: Optional[date] = Field(None, description="Tour start date")
    end_date: Optional[date] = Field(None, description="Tour end date")
    status: TourStatus = Field(TourStatus.DRAFT, description="Tour status")
    tags: List[str] = Field(default_factory=list, description="Tour tags")
    
    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip().title()
    
    @validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price cannot be negative')
        return v
    
    @root_validator
    def validate_dates(cls, values):
        start_date = values.get('start_date')
        end_date = values.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise ValueError('End date must be after start date')
            
            duration_days = values.get('duration_days')
            if duration_days:
                expected_duration = (end_date - start_date).days
                if abs(expected_duration - duration_days) > 1:
                    raise ValueError('Duration days should match the date range')
        
        return values
    
    @validator('tags')
    def validate_tags(cls, v):
        # Remove duplicates and empty tags
        return list(set(tag.strip().lower() for tag in v if tag.strip()))
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "title": "Amazing Paris Tour",
                "description": "Explore the beautiful city of Paris",
                "location": "Paris, France",
                "duration_days": 3,
                "max_participants": 20,
                "price": 50000,
                "start_date": "2024-06-01",
                "end_date": "2024-06-04",
                "status": "published",
                "tags": ["culture", "history", "food"]
            }
        }

class PaginationSchema(BaseModel):
    """Schema for pagination metadata"""
    page: int = Field(1, ge=1, description="Current page number")
    size: int = Field(10, ge=1, le=100, description="Items per page")
    total: int = Field(0, ge=0, description="Total number of items")
    pages: int = Field(0, ge=0, description="Total number of pages")
    
    @root_validator
    def calculate_pages(cls, values):
        total = values.get('total', 0)
        size = values.get('size', 10)
        values['pages'] = (total + size - 1) // size if total > 0 else 0
        return values

class PaginatedResponse(BaseModel):
    """Generic paginated response schema"""
    items: List[BaseModel]
    pagination: PaginationSchema
    
    class Config:
        from_attributes = True
