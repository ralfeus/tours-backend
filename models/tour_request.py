from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from .enums import RequestStatus

class TourRequest(Base):
    __tablename__ = "tour_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tour_id = Column(Integer, ForeignKey("tours.id"), nullable=False)
    participants_count = Column(Integer, nullable=False, default=1)
    preferred_date = Column(DateTime, nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="tour_requests")
    tour = relationship("Tour", back_populates="tour_requests")
