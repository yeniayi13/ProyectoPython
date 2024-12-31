from sqlalchemy import Column, Float, String, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from src.common.infrastructure.config.database.database import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(String(250), primary_key = True)
    first_name = Column(String(30),nullable = False)
    name = Column(String(30),nullable = False)
    brand = Column(String(30),nullable = False)
    price = Column(String(30),nullable = False)
    created_at = Column(DateTime, default=datetime, nullable=False)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime, nullable=False)
    #status = Column(
    #    String(8),
    #    CheckConstraint(
    #        "status IN ('ACTIVE', 'INACTIVE')",
    #        name='product_status_check'
    #    ),
    #    nullable=False
    #)


