from sqlalchemy import Column, Float, ForeignKey, String, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import uuid
from src.common.infrastructure.config.database.database import Base

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(String(250), primary_key = True)
    client_id = Column(String(250), ForeignKey('clients.id'))  
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(
        String(10),
        CheckConstraint(
            "status IN ('PENDING', 'COMPLETED', 'CANCELLED')",
            name='order_status_check'
        ),
        nullable=False
    )


