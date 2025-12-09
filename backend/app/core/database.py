from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Configure engine based on database type
if settings.DATABASE_URL.startswith("postgresql"):
    # PostgreSQL configuration with connection pooling
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=5,           # Number of connections to keep open
        max_overflow=10,       # Max connections beyond pool_size
        pool_pre_ping=True,    # Verify connections before using them
        pool_recycle=3600,     # Recycle connections after 1 hour
    )
else:
    # SQLite configuration (for local development)
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}  # Required for SQLite
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
