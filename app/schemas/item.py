from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.category import CategoryResponse


class ItemCreate(BaseModel):
    name: str
    sku: str
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category_id: int


class ItemUpdate(BaseModel):
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)


class ItemResponse(BaseModel):
    id: int
    name: str
    sku: str
    price: float
    stock: int
    created_at: datetime
    category: CategoryResponse

    class Config:
        from_attributes = True
