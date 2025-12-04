from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pwdlib import PasswordHash

from ..schemas.user_schemas import UserResponse, UserCreate, UserUpdate
from ..config.db import get_async_session
from ..models.user_model import User


Password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return Password_hasher.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return Password_hasher.verify(plain_password, hashed_password)

async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_async_session)) -> UserResponse:
    """Create a new user"""
    # Check if username or email already exists
    query = select(User).where((User.email == user_data.email))
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        if getattr(existing_user, "email", None) == user_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    print(hashed_password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return UserResponse( 
        id=getattr(db_user, "id"),
        email=getattr(db_user, "email"),
        created_at=getattr(db_user, "created_at")
    )

async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> List[UserResponse]:
    """Get all users with pagination"""
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return [
        UserResponse(
            id=getattr(user, "id"),
            email=getattr(user, "email"),
            created_at=getattr(user, "created_at")
        ) for user in users
    ]

async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_async_session)) -> UserResponse:
    """Get a user by ID"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return UserResponse(
        id=getattr(user, "id"),
        email=getattr(user, "email"),
        created_at=getattr(user, "created_at")
    )

async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_async_session)) -> UserResponse:
    """Update a user"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Chequear si el nuevo email ya existe en otros usuarios
    if user_data.email and user_data.email != getattr(user, "email"):
        query_check = select(User).where(User.email == user_data.email)
        result_check = await db.execute(query_check)
        if result_check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already taken")
        setattr(user, "email", user_data.email)
    
    if user_data.password:
        setattr(user, "hashed_password", hash_password(user_data.password))
    
    await db.commit()
    await db.refresh(user)
    
    return UserResponse(
        id=getattr(user, "id"),
        email=getattr(user, "email"),
        created_at=getattr(user, "created_at")
    )

async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)) -> dict:
    """Delete a user"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    await db.delete(user)
    await db.commit()
    
    return {"message": f"Usuario {getattr(user, 'email')} eliminado exitosamente"}