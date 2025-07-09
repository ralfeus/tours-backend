from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from models import RequestStatus
from .base import BaseSchema, TimestampMixin

class TourRequestBase(BaseSchema):
    tour_id: int = Field(..., gt=0)
    participants_count: int = Field(default=1, gt=0, le=50)
    preferred_date: datetime
    notes: Optional[str] = Field(None, max_length=1000)

class TourRequestCreate(TourRequestBase):
    @validator('preferred_date')
    def validate_preferred_date(cls, v):
        if v <= datetime.now():
            raise ValueError('Preferred date must be in the future')
        return v
    
    @validator('notes')
    def validate_notes(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else v

class TourRequestUpdate(BaseModel):
    participants_count: Optional[int] = Field(None, gt=0, le=50)
    preferred_date: Optional[datetime] = None
    status: Optional[RequestStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)
    
    @validator('preferred_date')
    def validate_preferred_date(cls, v):
        if v and v <= datetime.now():
            raise ValueError('Preferred date must be in the future')
        return v
    
    @validator('notes')
    def validate_notes(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else v

class TourRequest(TourRequestBase, TimestampMixin):
    id: int
    user_id: int
    status: RequestStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
