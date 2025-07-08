from pydantic import BaseModel, validator
from datetime import datetime
from .base import BaseSchema
from .user import User
from .tour import Tour

class FeedbackBase(BaseModel):
    tour_id: int
    rating: int
    comment: str | None = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None
    is_published: bool | None = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class Feedback(FeedbackBase):
    id: int
    user_id: int
    is_published: bool
    created_at: datetime
    updated_at: datetime
    user: User
    tour: Tour
    
    class Config:
        from_attributes = True
