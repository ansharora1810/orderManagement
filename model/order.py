from enum import Enum
from typing import List
from pydantic import UUID4, BaseModel
from model.order_item import OrderItem


class OrderStatus(int, Enum):
    PENDING = 0
    CANCELLED = 1
    SUCCESS = 2


class Order(BaseModel):
    order_items: List[OrderItem]
    user_id: UUID4
    total_value: int
    status: OrderStatus

