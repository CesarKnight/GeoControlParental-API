from pydantic import BaseModel, EmailStr, Field, field_validator, validator
from typing import Optional
from datetime import datetime
import re
    
class UserResponse(BaseModel):
    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="Valid email address")
    created_at: datetime = Field(..., description="User creation timestamp")

    class Config:
        from_attributes = True  # Updated for Pydantic v2 (replaces orm_mode)
            
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=128, description="Password must be at least 8 characters")
    
    @field_validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    
    @field_validator('password')
    def validate_password(cls, v):
        if v is not None:
            if not re.search(r'[A-Za-z]', v):
                raise ValueError('Password must contain at least one letter')
            if not re.search(r'\d', v):
                raise ValueError('Password must contain at least one number')
        return v
        
class UserLogin(BaseModel):
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")

class UserPasswordChange(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    
    @field_validator('new_password')
    def validate_new_password(cls, v):
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v