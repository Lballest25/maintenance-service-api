from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    report_text: str
    items: List[OrderItemCreate]
    image_url: Optional[str] = None


class OrderItemResponse(BaseModel):
    item_id: int
    quantity: int
    unit_price: float


class OrderResponse(BaseModel):
    id: int
    report_text: str
    image_url: Optional[str]
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
