from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Integer,Text, ForeignKey, DateTime, PrimaryKeyConstraint
from datetime import datetime
from ..config.db import Base

class User(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)