"""
Database connection and session management with profile-based configuration
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from src.models.user import Base
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Get database URL from profile-based settings
if "pytest" in os.environ.get("_", "") or "PYTEST_CURRENT_TEST" in os.environ:
    DATABASE_URL = "sqlite:///:memory:"
    logger.info("🧪 TEST: Using in-memory SQLite for testing")
else:
    DATABASE_URL = settings.effective_database_url

# Create engine
if DATABASE_URL.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # PostgreSQL configuration
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def create_tables():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database (for testing/development)
def init_db():
    """Initialize database with tables"""
    try:
        create_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
