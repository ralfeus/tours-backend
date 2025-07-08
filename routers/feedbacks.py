from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Feedback, Tour, UserRole
from schemas import (
    Feedback as FeedbackSchema, 
    FeedbackCreate, 
    FeedbackUpdate, 
    CurrentUser
)
from auth import get_current_user

router = APIRouter()

@router.get("", response_model=List[FeedbackSchema])
async def get_feedbacks(
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user)
):
    """Get feedbacks - Published for anyone, unpublished only for admin"""
    if current_user and current_user.role == UserRole.ADMIN:
        return db.query(Feedback).all()
    else:
        return db.query(Feedback).filter(Feedback.is_published == True).all()

@router.get("/{feedback_id}", response_model=FeedbackSchema)
async def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user)
):
    """Get feedback by ID - Published for anyone, unpublished only for admin"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    if not feedback.is_published and (not current_user or current_user.role != UserRole.ADMIN):
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    return feedback

@router.post("", response_model=FeedbackSchema)
async def create_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Create feedback - Anyone can create, tour association mandatory"""
    # Verify tour exists
    tour = db.query(Tour).filter(Tour.id == feedback_data.tour_id, Tour.is_active == True).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found or inactive")
    
    feedback = Feedback(**feedback_data.dict(), user_id=current_user.id)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

@router.put("/{feedback_id}", response_model=FeedbackSchema)
async def update_feedback(
    feedback_id: int,
    feedback_data: FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Update feedback - Admin updates any, others only their own"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    if current_user.role != UserRole.ADMIN and feedback.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    update_data = feedback_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(feedback, field, value)
    
    feedback.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(feedback)
    return feedback

@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Delete feedback - Admin deletes any, others only their own"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    if current_user.role != UserRole.ADMIN and feedback.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(feedback)
    db.commit()
    return {"message": "Feedback deleted successfully"}
