from pydantic import BaseModel
from datetime import datetime
from models import RequestStatus
from .base import BaseSchema
from .user import User
from .tour import Tour

class TourRequestBase(BaseModel):
    tour_id: int
    participants_count: int = 1
    preferred_date: datetime
    notes: str | None = None

class TourRequestCreate(TourRequestBase):
    pass

class TourRequestUpdate(BaseModel):
    participants_count: int | None = None
    preferred_date: datetime | None = None
    status: RequestStatus | None = None
    notes: str | None = None

class TourRequest(TourRequestBase):
    id: int
    user_id: int
    status: RequestStatus
    created_at: datetime
    updated_at: datetime
    user: User
    tour: Tour
    
    class Config:
        from_attributes = True
