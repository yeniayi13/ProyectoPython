from uuid import UUID, uuid4
from typing import Optional

class OrderItem:
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int

    def __init__(self, order_id: UUID, product_id: UUID, quantity: int):
        self.id = uuid4()
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

