from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Integer,Text, ForeignKey, DateTime, PrimaryKeyConstraint
from datetime import datetime
from ..config.db import Base

class User(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    