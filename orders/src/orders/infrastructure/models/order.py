from sqlalchemy import Column, Float, String, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from src.common.infrastructure.config.database.database import Base

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime, nullable=False)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(
        String(10),
        CheckConstraint(
            "status IN ('pending', 'completed', 'cancelled')",
            name='status_check'
        ),
        nullable=False
    )
