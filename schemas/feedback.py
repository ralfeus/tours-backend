from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from .base import BaseSchema, TimestampMixin

class FeedbackBase(BaseSchema):
    tour_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    comment: Optional[str] = Field(None, max_length=2000)
    is_published: bool = False

class FeedbackCreate(FeedbackBase):
    @validator('rating')
    def validate_rating(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v
    
    @validator('comment')
    def validate_comment(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else v

class FeedbackUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=2000)
    is_published: Optional[bool] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v
    
    @validator('comment')
    def validate_comment(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else v

class Feedback(FeedbackBase, TimestampMixin):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
