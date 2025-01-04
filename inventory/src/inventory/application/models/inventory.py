from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

class Inventory:
    id: UUID
    product_id: UUID
    quantity: int
    created_at: str
    updated_at: str

    def __init__(self, product_id: UUID, quantity: int, created_at: Optional[str] = None, updated_at: Optional[str] = None):
        self.id = uuid4()
        self.product_id = product_id
        self.quantity = quantity
        self.created_at = created_at if created_at else datetime.utcnow().isoformat()
        self.updated_at = updated_at if updated_at else datetime.utcnow().isoformat()

    def __str__(self):
        return f"Inventory(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, created_at={self.created_at}, updated_at={self.updated_at})"
