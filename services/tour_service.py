from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any

from models import Tour, TourRequest, RequestStatus
from schemas import TourStats

class TourService:
    """Service for tour-related business logic"""
    
    @staticmethod
    def get_tour_statistics(db: Session) -> TourStats:
        """Get basic tour statistics"""
        # Get tour counts
        total_tours = db.query(Tour).count()
        active_tours = db.query(Tour).filter(Tour.is_active == True).count()
        inactive_tours = total_tours - active_tours
        
        # Get participants count from approved and pending requests for active tours
        participants_query = db.query(func.sum(TourRequest.participants_count)).join(Tour).filter(
            Tour.is_active == True,
            TourRequest.status.in_([RequestStatus.APPROVED, RequestStatus.PENDING])
        ).scalar()
        
        participants = participants_query or 0
        
        return TourStats(
            total=total_tours,
            active=active_tours,
            inactive=inactive_tours,
            participants=participants
        )
    
    @staticmethod
    def get_detailed_tour_statistics(db: Session) -> Dict[str, Any]:
        """Get detailed tour statistics with additional metrics"""
        basic_stats = TourService.get_tour_statistics(db)
        
        # Calculate average participants per tour
        active_tours_count = basic_stats.active
        avg_participants = (basic_stats.participants / active_tours_count) if active_tours_count > 0 else 0
        
        # Find most popular tour (by request count)
        most_popular_query = db.query(
            Tour.title,
            func.count(TourRequest.id).label('request_count')
        ).join(TourRequest).filter(
            Tour.is_active == True
        ).group_by(Tour.id, Tour.title).order_by(
            func.count(TourRequest.id).desc()
        ).first()
        
        most_popular_tour = most_popular_query.title if most_popular_query else None
        most_popular_requests = most_popular_query.request_count if most_popular_query else 0
        
        return {
            "total": basic_stats.total,
            "active": basic_stats.active,
            "inactive": basic_stats.inactive,
            "participants": basic_stats.participants,
            "average_participants_per_tour": round(avg_participants, 2),
            "most_popular_tour": most_popular_tour,
            "most_popular_tour_requests": most_popular_requests
        }
