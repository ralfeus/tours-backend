from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TimestampMixin(BaseModel):
    """Mixin for models with timestamp fields"""
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    class Config:
        from_attributes = True
