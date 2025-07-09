from .base import BaseSchema, TimestampMixin
from .user import User, UserBase, UserCreate, UserUpdate
from .tour import Tour, TourBase, TourCreate, TourUpdate, TourStats
from .tour_request import TourRequest, TourRequestBase, TourRequestCreate, TourRequestUpdate
from .feedback import Feedback, FeedbackBase, FeedbackCreate, FeedbackUpdate
from .auth import CurrentUser

# Export all schemas for easy importing
__all__ = [
    # Base schemas
    "BaseSchema",
    "TimestampMixin",
    
    # User schemas
    "User",
    "UserBase", 
    "UserCreate",
    "UserUpdate",
    
    # Tour schemas
    "Tour",
    "TourBase",
    "TourCreate", 
    "TourUpdate",
    "TourStats",
    
    # Tour Request schemas
    "TourRequest",
    "TourRequestBase",
    "TourRequestCreate",
    "TourRequestUpdate",
    
    # Feedback schemas
    "Feedback",
    "FeedbackBase",
    "FeedbackCreate",
    "FeedbackUpdate",
    
    # Auth schemas
    "CurrentUser"
]
