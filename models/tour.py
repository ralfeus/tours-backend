from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Tour(Base):
    __tablename__ = "tours"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    location = Column(String(200), nullable=False)
    duration_days = Column(Integer, nullable=False)
    max_participants = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)  # Price in cents
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tour_requests = relationship("TourRequest", back_populates="tour", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="tour", cascade="all, delete-orphan")
