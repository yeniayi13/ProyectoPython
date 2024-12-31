from sqlalchemy import Column, Float, String, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from src.common.infrastructure.config.database.database import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column(String(250), primary_key = True)
    first_name = Column(String(30),nullable = False)
    last_name = Column(String(30),nullable = False)
    c_i = Column(String(10),unique= True, nullable=False)
    email = Column(String(50), unique= True, nullable = False)
    created_at = Column(DateTime, default=datetime, nullable=False)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime, nullable=False)


