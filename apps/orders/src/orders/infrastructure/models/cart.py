from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from src.common.infrastructure.config.database.database import Base
import uuid

class Cart(Base):
    __tablename__ = 'carts'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(String(250), ForeignKey('clients.id'), nullable=False)  
    product_id = Column(String(250), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
