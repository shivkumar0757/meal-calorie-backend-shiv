"""
SQLAlchemy User model
"""
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Create base class for models
Base = declarative_base()


class User(Base):
    """User model for authentication and user management"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
    
    @classmethod 
    def get_by_email(cls, db: Session, email: str) -> Optional["User"]:
        """Get user by email address"""
        return db.query(cls).filter(cls.email == email).first()
    
    @classmethod
    def get_by_id(cls, db: Session, user_id: int) -> Optional["User"]:
        """Get user by ID"""
        return db.query(cls).filter(cls.id == user_id).first()
    
    @classmethod
    def create(cls, db: Session, **kwargs) -> "User":
        """Create a new user"""
        user = cls(**kwargs)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Created user: {user.email}")
        return user
    
    def to_dict(self) -> dict:
        """Convert user to dictionary (without password)"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
