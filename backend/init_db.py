"""
Database initialization script
Run this to create all tables in the database
"""
from app.core.database import engine, Base
from app.models.models import User, Workout, Exercise, NutritionLog, Goal

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print("\nCreated tables:")
    print("  - users")
    print("  - workouts")
    print("  - exercises")
    print("  - nutrition_logs")
    print("  - goals")

if __name__ == "__main__":
    init_db()
