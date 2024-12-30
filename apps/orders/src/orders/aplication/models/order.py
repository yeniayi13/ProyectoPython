from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import Optional

class Status(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order:
    id: UUID
    user_id: UUID
    total_amount: float
    status: Status
    created_at: str
    updated_at: str

    def __init__(self, user_id: UUID, total_amount: float, status: Status, created_at: Optional[str] = None, updated_at: Optional[str] = None):
        self.id = uuid4()
        self.user_id = user_id
        self.total_amount = total_amount
        self.status = status
        self.created_at = created_at if created_at else datetime.utcnow().isoformat()
        self.updated_at = updated_at if updated_at else datetime.utcnow().isoformat()
