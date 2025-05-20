from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    categories: str
    rating: float
    brand: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    categories: Optional[str] = None
    rating: Optional[float] = None
    brand: Optional[str] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
