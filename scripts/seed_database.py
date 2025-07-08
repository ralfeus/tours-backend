from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, Tour, UserRole
from services.auth_service import AuthService
from datetime import datetime, timedelta

def seed_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        if db.query(User).first():
            print("Database already seeded!")
            return
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@example.com",
            full_name="System Administrator",
            role=UserRole.ADMIN,
            hashed_password=AuthService.hash_password("admin123")
        )
        db.add(admin_user)
        
        # Create leader user
        leader_user = User(
            username="leader",
            email="leader@example.com",
            full_name="Tour Leader",
            role=UserRole.LEADER,
            hashed_password=AuthService.hash_password("leader123")
        )
        db.add(leader_user)
        
        # Create requestor user
        requestor_user = User(
            username="requestor",
            email="requestor@example.com",
            full_name="Tour Requestor",
            role=UserRole.REQUESTOR,
            hashed_password=AuthService.hash_password("requestor123")
        )
        db.add(requestor_user)
        
        # Create sample tours
        tours = [
            Tour(
                title="Paris City Tour",
                description="Explore the beautiful city of Paris with our expert guides",
                location="Paris, France",
                duration_days=3,
                max_participants=20,
                price=50000  # $500.00 in cents
            ),
            Tour(
                title="Tokyo Adventure",
                description="Experience the vibrant culture of Tokyo",
                location="Tokyo, Japan",
                duration_days=5,
                max_participants=15,
                price=80000  # $800.00 in cents
            ),
            Tour(
                title="New York Highlights",
                description="See the best of the Big Apple",
                location="New York, USA",
                duration_days=4,
                max_participants=25,
                price=60000  # $600.00 in cents
            )
        ]
        
        for tour in tours:
            db.add(tour)
        
        db.commit()
        print("Database seeded successfully!")
        print("Default users created:")
        print("- Admin: username='admin', password='admin123'")
        print("- Leader: username='leader', password='leader123'")
        print("- Requestor: username='requestor', password='requestor123'")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
