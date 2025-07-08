from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import TourRequest, Tour, UserRole
from schemas import (
    TourRequest as TourRequestSchema, 
    TourRequestCreate, 
    TourRequestUpdate, 
    CurrentUser
)
from auth import get_current_user

router = APIRouter()

@router.get("", response_model=List[TourRequestSchema])
async def get_requests(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get tour requests - Admin gets all, others get only their own"""
    if current_user.role == UserRole.ADMIN:
        return db.query(TourRequest).all()
    else:
        return db.query(TourRequest).filter(TourRequest.user_id == current_user.id).all()

@router.get("/{request_id}", response_model=TourRequestSchema)
async def get_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get tour request by ID - Admin gets any, others only their own"""
    request = db.query(TourRequest).filter(TourRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if current_user.role != UserRole.ADMIN and request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return request

@router.post("", response_model=TourRequestSchema)
async def create_request(
    request_data: TourRequestCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Create a new tour request - Available to anyone"""
    # Verify tour exists
    tour = db.query(Tour).filter(Tour.id == request_data.tour_id, Tour.is_active == True).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found or inactive")
    
    request = TourRequest(**request_data.dict(), user_id=current_user.id)
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

@router.put("/{request_id}", response_model=TourRequestSchema)
async def update_request(
    request_id: int,
    request_data: TourRequestUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Update tour request - Admin updates any, others only their own"""
    request = db.query(TourRequest).filter(TourRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if current_user.role != UserRole.ADMIN and request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    update_data = request_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(request, field, value)
    
    request.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(request)
    return request

@router.delete("/{request_id}")
async def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Cancel/delete tour request - Admin cancels any, others only their own"""
    request = db.query(TourRequest).filter(TourRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if current_user.role != UserRole.ADMIN and request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(request)
    db.commit()
    return {"message": "Request cancelled successfully"}
