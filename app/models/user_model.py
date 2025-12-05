from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Integer,Text, ForeignKey, DateTime, PrimaryKeyConstraint
from datetime import datetime
from ..config.db import Base
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass