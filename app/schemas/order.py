from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List
from app.models.order import OrderType, OrderStatus

class OrderItemInput(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)

class CreateOrder(BaseModel):
    order_type: OrderType
    items: List[OrderItemInput]

class OutOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    status: OrderStatus
    order_type: OrderType
    original_total_price: int
    final_total_price: int
    total_prepare_time: int
    updated_at: datetime
    created_at: datetime
