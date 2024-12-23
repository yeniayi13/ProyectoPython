from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

class Product:
    id: UUID
    code: str
    name: str
    description: Optional[str]
    cost: float
    margin: float
    price: float
    created_at: str
    updated_at: str

    def __init__(self, code: str, name: str, description: Optional[str], cost: float, margin: float, price: float, created_at: Optional[str] = None, updated_at: Optional[str] = None):
        self.id = uuid4()
        self.code = code
        self.name = name
        self.description = description
        self.cost = cost
        self.margin = margin
        self.price = price
        self.created_at = created_at if created_at else datetime.utcnow().isoformat()
        self.updated_at = updated_at if updated_at else datetime.utcnow().isoformat()

    def __str__(self):
        return f"Product(id={self.id}, code={self.code}, name={self.name}, description={self.description}, cost={self.cost}, margin={self.margin}, price={self.price}, created_at={self.created_at}, updated_at={self.updated_at})"
