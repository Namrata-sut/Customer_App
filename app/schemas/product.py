from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Integer


class ProductSchema(BaseModel):
    name: str
    price: float
    stock: int

    class Config:
        from_attributes = True


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
