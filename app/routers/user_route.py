from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..controllers import user_controller
from ..schemas.user_schemas import UserResponse, UserCreate, UserUpdate
from ..config.db import get_async_session

router = APIRouter(prefix="/users", tags=["users"])
@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Crear un nuevo usuario"""
    return await user_controller.create_user(user_data, db)


@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = Query(0, ge=0, description="Salto de registros"),
    limit: int = Query(100, ge=1, le=1000, description="Número de usuarios a devolver"),
    db: AsyncSession = Depends(get_async_session)
):
    """Obtener todos los usuarios con paginación"""
    return await user_controller.get_users(skip, limit, db)


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Obtener un usuario por ID"""
    return await user_controller.get_user_by_id(user_id, db)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Actualizar un usuario"""
    return await user_controller.update_user(user_id, user_data, db)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Eliminar un usuario"""
    return await user_controller.delete_user(user_id, db)
