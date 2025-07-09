import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, Tour, TourRequest, Feedback, UserRole, RequestStatus
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_data():
    """Create sample data for the tours management system"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Feedback).delete()
        db.query(TourRequest).delete()
        db.query(Tour).delete()
        db.query(User).delete()
        db.commit()
        
        logger.info("Creating sample users...")
        
        # Create sample users
        users = [
            User(
                username="admin",
                email="admin@example.com",
                full_name="System Administrator",
                hashed_password=User.hash_password("admin123"),
                role=UserRole.ADMIN,
                is_active=True
            ),
            User(
                username="leader",
                email="leader@example.com",
                full_name="Tour Leader",
                hashed_password=User.hash_password("leader123"),
                role=UserRole.LEADER,
                is_active=True
            ),
            User(
                username="requestor",
                email="requestor@example.com",
                full_name="Tour Requestor",
                hashed_password=User.hash_password("requestor123"),
                role=UserRole.REQUESTOR,
                is_active=True
            ),
            User(
                username="john_doe",
                email="john@example.com",
                full_name="John Doe",
                hashed_password=User.hash_password("password123"),
                role=UserRole.REQUESTOR,
                is_active=True
            ),
            User(
                username="jane_smith",
                email="jane@example.com",
                full_name="Jane Smith",
                hashed_password=User.hash_password("password123"),
                role=UserRole.REQUESTOR,
                is_active=True
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        logger.info("Creating sample tours...")
        
        # Create sample tours
        tours = [
            Tour(
                title="Paris City Tour",
                description="Explore the beautiful city of Paris with our expert guides. Visit the Eiffel Tower, Louvre Museum, and more!",
                location="Paris, France",
                duration_days=3,
                max_participants=20,
                price=29900,  # $299.00
                is_active=True
            ),
            Tour(
                title="Tokyo Adventure",
                description="Experience the vibrant culture of Tokyo. From traditional temples to modern skyscrapers.",
                location="Tokyo, Japan",
                duration_days=5,
                max_participants=15,
                price=49900,  # $499.00
                is_active=True
            ),
            Tour(
                title="New York Highlights",
                description="See the best of NYC including Times Square, Central Park, and the Statue of Liberty.",
                location="New York, USA",
                duration_days=4,
                max_participants=25,
                price=39900,  # $399.00
                is_active=True
            ),
            Tour(
                title="London Historical Tour",
                description="Discover London's rich history with visits to the Tower of London, Big Ben, and Buckingham Palace.",
                location="London, UK",
                duration_days=3,
                max_participants=18,
                price=34900,  # $349.00
                is_active=False  # Inactive tour for testing
            )
        ]
        
        for tour in tours:
            db.add(tour)
        db.commit()
        
        logger.info("Creating sample tour requests...")
        
        # Create sample tour requests
        requests = [
            TourRequest(
                user_id=3,  # requestor
                tour_id=1,  # Paris tour
                participants_count=2,
                preferred_date=datetime.now() + timedelta(days=30),
                status=RequestStatus.PENDING,
                notes="Looking forward to this trip!"
            ),
            TourRequest(
                user_id=4,  # john_doe
                tour_id=1,  # Paris tour
                participants_count=1,
                preferred_date=datetime.now() + timedelta(days=45),
                status=RequestStatus.APPROVED,
                notes="Solo traveler"
            ),
            TourRequest(
                user_id=5,  # jane_smith
                tour_id=2,  # Tokyo tour
                participants_count=3,
                preferred_date=datetime.now() + timedelta(days=60),
                status=RequestStatus.PENDING,
                notes="Family trip with kids"
            ),
            TourRequest(
                user_id=3,  # requestor
                tour_id=3,  # New York tour
                participants_count=2,
                preferred_date=datetime.now() + timedelta(days=90),
                status=RequestStatus.APPROVED,
                notes="Anniversary trip"
            ),
            TourRequest(
                user_id=4,  # john_doe
                tour_id=2,  # Tokyo tour
                participants_count=1,
                preferred_date=datetime.now() + timedelta(days=120),
                status=RequestStatus.REJECTED,
                notes="Business trip"
            )
        ]
        
        for request in requests:
            db.add(request)
        db.commit()
        
        logger.info("Creating sample feedback...")
        
        # Create sample feedback
        feedbacks = [
            Feedback(
                user_id=4,  # john_doe
                tour_id=1,  # Paris tour
                rating=5,
                comment="Amazing tour! The guide was very knowledgeable and the itinerary was perfect.",
                is_published=True
            ),
            Feedback(
                user_id=3,  # requestor
                tour_id=3,  # New York tour
                rating=4,
                comment="Great experience overall. Would recommend to others.",
                is_published=True
            ),
            Feedback(
                user_id=5,  # jane_smith
                tour_id=2,  # Tokyo tour
                rating=5,
                comment="Incredible journey through Tokyo. The cultural experiences were unforgettable!",
                is_published=False  # Unpublished feedback
            )
        ]
        
        for feedback in feedbacks:
            db.add(feedback)
        db.commit()
        
        logger.info("Sample data created successfully!")
        
        # Print summary
        user_count = db.query(User).count()
        tour_count = db.query(Tour).count()
        request_count = db.query(TourRequest).count()
        feedback_count = db.query(Feedback).count()
        
        logger.info(f"Created {user_count} users, {tour_count} tours, {request_count} requests, {feedback_count} feedbacks")
        
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
