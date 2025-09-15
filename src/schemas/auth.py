"""
Pydantic schemas for authentication
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    """Schema for user registration"""

    first_name: str = Field(
        ..., min_length=1, max_length=50, description="User's first name"
    )
    last_name: str = Field(
        ..., min_length=1, max_length=50, description="User's last name"
    )
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ..., min_length=6, max_length=100, description="User's password"
    )


class UserLogin(BaseModel):
    """Schema for user login"""

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ..., min_length=6, max_length=100, description="User's password"
    )


class UserResponse(BaseModel):
    """Schema for user data in responses"""

    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for JWT token response"""

    access_token: str
    token_type: str = "bearer"
    user: Optional[UserResponse] = None


class Token(BaseModel):
    """Schema for JWT token data"""

    sub: str  # subject (user_id)
    exp: int  # expiration time
