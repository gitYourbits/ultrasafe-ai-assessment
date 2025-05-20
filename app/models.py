from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class ProductORM(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    categories = Column(String, nullable=False)
    rating = Column(Float, nullable=True)
    brand = Column(String, nullable=True)

# Pydantic models for validation
class Product(BaseModel):
    name: str
    description: str
    price: float
    categories: str
    rating: float
    brand: str

class ProductOut(Product):
    id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    categories: Optional[str] = None
    rating: Optional[float] = None
    brand: Optional[str] = None
