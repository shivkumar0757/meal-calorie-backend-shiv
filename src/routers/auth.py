"""
Authentication endpoints for user registration and login
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.schemas.auth import UserCreate, UserLogin, TokenResponse, UserResponse
from src.models.user import User
from src.database.connection import get_db
from src.utils.auth import verify_password, get_password_hash, create_access_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "Email already registered"},
        422: {"description": "Validation error"}
    }
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account
    
    Creates a new user with hashed password and returns JWT access token
    """
    try:
        logger.info(f"User registration attempt: {user_data.email}")
        
        # Check if user already exists
        existing_user = User.get_by_email(db, user_data.email)
        if existing_user:
            logger.warning(f"Registration failed - email already exists: {user_data.email}")
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": "Email already registered"}
            )
        
        # Hash password
        password_hash = get_password_hash(user_data.password)
        
        # Create user
        new_user = User.create(
            db=db,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password_hash=password_hash
        )
        
        # Create access token
        access_token = create_access_token(data={"sub": str(new_user.id)})
        
        # Prepare response
        user_response = UserResponse(
            id=new_user.id,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email
        )
        
        response = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
        logger.info(f"User registered successfully: {new_user.email}")
        return response
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error during registration"}
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        401: {"description": "Invalid credentials"},
        422: {"description": "Validation error"}
    }
)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT access token
    
    Authenticates user credentials and returns access token for API access
    """
    try:
        logger.info(f"Login attempt: {credentials.email}")
        
        # Get user by email
        user = User.get_by_email(db, credentials.email)
        if not user:
            logger.warning(f"Login failed - user not found: {credentials.email}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid email or password"}
            )
        
        # Verify password
        if not verify_password(credentials.password, user.password_hash):
            logger.warning(f"Login failed - invalid password: {credentials.email}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid email or password"}
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        # Prepare response
        user_response = UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
        
        response = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
        logger.info(f"Login successful: {user.email}")
        return response
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error during login"}
        )
