import os
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import logging

# Todo construir la URL de la base de datos desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app/config/test.db")

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Engine configuration
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("LOG_DB_QUERIES", "false").lower() == "true",  # Logear consultas en Dev
    future=True,
    pool_pre_ping=True if "sqlite" not in DATABASE_URL else False,
)

async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_db_and_tables():
    try:
        # Importar todos los modelos necesarios
        from ..models import user_model
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise
    
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:    
        yield session