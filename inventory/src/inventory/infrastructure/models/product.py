from sqlalchemy import Column, String, Text, Float, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from src.common.infrastructure.config.database.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    cost = Column(Float, nullable=False)
    margin = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


