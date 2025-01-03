from sqlalchemy import Column, Float, Integer, String, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import uuid
from src.common.infrastructure.config.database.database import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(String(250), primary_key = True)
    name = Column(String(30),nullable = False)
    quantity = Column(Integer,nullable = False)
    price = Column(String(30),nullable = False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    #status = Column(
    #    String(8),
    #    CheckConstraint(
    #        "status IN ('ACTIVE', 'INACTIVE')",
    #        name='product_status_check'
    #    ),
    #    nullable=False
    #)


