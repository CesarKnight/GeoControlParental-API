from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from typing import List, Optional

from ..schemas.user_schemas import UserResponse, UserCreate, UserUpdate
from ..config.db import get_async_session
from ..models.user_model import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_async_session)) -> UserResponse:
    """Create a new user"""
    # Check if username or email already exists
    stmt = select(User).where((User.username == user_data.username) | (User.email == user_data.email))
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        if getattr(existing_user, "username", None) == user_data.username:
            raise HTTPException(status_code=400, detail="Username already registered")
        if getattr(existing_user, "email", None) == user_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return UserResponse( 
        id=getattr(db_user, "id"),
        username=getattr(db_user, "username"),
        email=getattr(db_user, "email"),
        full_name=getattr(db_user, "full_name"),
        is_active=bool(getattr(db_user, "is_active")),
        created_at=getattr(db_user, "created_at")
    )

async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> List[UserResponse]:
    """Get all users with pagination"""
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    users = result.scalars().all()
    
    return [
        UserResponse(
            id=getattr(user, "id"),
            username=getattr(user, "username"),
            email=getattr(user, "email"),
            full_name=getattr(user, "full_name"),
            is_active=bool(getattr(user, "is_active")),
            created_at=getattr(user, "created_at")
        ) for user in users
    ]

async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_async_session)) -> UserResponse:
    """Get a user by ID"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=getattr(user, "id"),
        username=getattr(user, "username"),
        email=getattr(user, "email"),
        full_name=getattr(user, "full_name"),
        is_active=bool(getattr(user, "is_active")),
        created_at=getattr(user, "created_at")
    )

async def get_user_by_username(username: str, db: AsyncSession = Depends(get_async_session)) -> UserResponse:
    """Get a user by username"""
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=getattr(user, "id"),
        username=getattr(user, "username"),
        email=getattr(user, "email"),
        full_name=getattr(user, "full_name"),
        is_active=bool(getattr(user, "is_active")),
        created_at=getattr(user, "created_at")
    )

async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_async_session)) -> UserResponse:
    """Update a user"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check for unique constraints if updating username or email
    if user_data.username and user_data.username != getattr(user, "username"):
        stmt_check = select(User).where(User.username == user_data.username)
        result_check = await db.execute(stmt_check)
        if result_check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already taken")
        setattr(user, "username", user_data.username)
    
    if user_data.email and user_data.email != getattr(user, "email"):
        stmt_check = select(User).where(User.email == user_data.email)
        result_check = await db.execute(stmt_check)
        if result_check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already taken")
        setattr(user, "email", user_data.email)
    
    # Update other fields
    if user_data.full_name is not None:
        setattr(user, "full_name", user_data.full_name)
    
    if user_data.password:
        setattr(user, "hashed_password", hash_password(user_data.password))
    
    if user_data.is_active is not None:
        setattr(user, "is_active", 1 if user_data.is_active else 0)
    
    await db.commit()
    await db.refresh(user)
    
    return UserResponse(
        id=getattr(user, "id"),
        username=getattr(user, "username"),
        email=getattr(user, "email"),
        full_name=getattr(user, "full_name"),
        is_active=bool(getattr(user, "is_active")),
        created_at=getattr(user, "created_at")
    )

async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)) -> dict:
    """Delete a user"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    
    return {"message": f"User {getattr(user, 'username')} deleted successfully"}

async def activate_user(user_id: int, db: AsyncSession = Depends(get_async_session)) -> UserResponse:
    """Activate a user"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    setattr(user, "is_active", 1)
    await db.commit()
    await db.refresh(user)
    
    return UserResponse(
        id=getattr(user, "id"),
        username=getattr(user, "username"),
        email=getattr(user, "email"),
        full_name=getattr(user, "full_name"),
        is_active=bool(getattr(user, "is_active")),
        created_at=getattr(user, "created_at")
    )

async def deactivate_user(user_id: int, db: AsyncSession = Depends(get_async_session)) -> UserResponse:
    """Deactivate a user"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    setattr(user, "is_active", 0)
    await db.commit()
    await db.refresh(user)
    
    return UserResponse(
        id=getattr(user, "id"),
        username=getattr(user, "username"),
        email=getattr(user, "email"),
        full_name=getattr(user, "full_name"),
        is_active=bool(getattr(user, "is_active")),
        created_at=getattr(user, "created_at")
    )