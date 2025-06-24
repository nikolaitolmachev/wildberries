from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    id_wb: int
    name: str
    price_basic: Optional[float] = None
    price_with_discount: Optional[float] = None
    rating: Optional[float] = None
    feedbacks: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ParseRequest(BaseModel):
    query: str = Field(..., example="футболка женская")
    pages: int = Field(1, ge=1, le=100, example=3)
