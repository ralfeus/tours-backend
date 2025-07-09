from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Tour
from schemas import Tour as TourSchema, TourCreate, TourUpdate, TourStats, CurrentUser
from auth import require_admin
from services.tour_service import TourService

router = APIRouter()

@router.get("", response_model=List[TourSchema])
async def get_tours(db: Session = Depends(get_db)):
    """Get all active tours - Available to anyone"""
    return db.query(Tour).filter(Tour.is_active == True).all()

@router.get("/{tour_id}", response_model=TourSchema)
async def get_tour(tour_id: int, db: Session = Depends(get_db)):
    """Get tour by ID - Available to anyone"""
    tour = db.query(Tour).filter(Tour.id == tour_id, Tour.is_active == True).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    return tour

@router.post("", response_model=TourSchema)
async def create_tour(
    tour_data: TourCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin)
):
    """Create a new tour - Admin only"""
    tour = Tour(**tour_data.dict())
    db.add(tour)
    db.commit()
    db.refresh(tour)
    return tour

@router.put("/{tour_id}", response_model=TourSchema)
async def update_tour(
    tour_id: int,
    tour_data: TourUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin)
):
    """Update tour - Admin only"""
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    
    update_data = tour_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tour, field, value)
    
    db.commit()
    db.refresh(tour)
    return tour

@router.delete("/{tour_id}")
async def delete_tour(
    tour_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin)
):
    """Delete tour - Admin only. Also deletes associated requests"""
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    
    db.delete(tour)  # Cascade will handle tour requests
    db.commit()
    return {"message": "Tour deleted successfully"}

@router.get("/stats", response_model=TourStats)
async def get_tour_stats(db: Session = Depends(get_db)):
    """Get tour statistics - Available to anyone"""
    return TourService.get_tour_statistics(db)

@router.get("/stats/detailed")
async def get_detailed_tour_stats(db: Session = Depends(get_db)):
    """Get detailed tour statistics with additional metrics - Available to anyone"""
    return TourService.get_detailed_tour_statistics(db)
