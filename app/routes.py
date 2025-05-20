from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal, semantic_search
from app.schemas import ProductCreate, ProductUpdate, ProductOut
from app.crud import get_products, get_product, create_product, update_product, delete_product
from app.models import ProductORM
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products", response_model=List[ProductOut], summary="List all products", description="List all products with pagination.")
def list_products(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    return get_products(db, skip, limit)

@router.get("/products/search", response_model=List[ProductOut], summary="Semantic search", description="Semantic search for products using a query string.")
def search_products(q: str = Query(..., description="Search query"), top_k: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    matched_ids = semantic_search(q, top_k)
    if not matched_ids:
        return []
    products = db.query(ProductORM).filter(ProductORM.id.in_(matched_ids)).all()
    # Return in the order of matched_ids
    id_to_product = {p.id: p for p in products}
    return [id_to_product[pid] for pid in matched_ids if pid in id_to_product]

@router.get("/products/{product_id}", response_model=ProductOut, summary="Get product details", description="Get details of a specific product by ID.")
def get_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/products", response_model=ProductOut, summary="Add a new product", description="Add a new product to the catalog.")
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.put("/products/{product_id}", response_model=ProductOut, summary="Update a product", description="Update an existing product by ID.")
def update_product_route(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    updated = update_product(db, product_id, product_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/products/{product_id}", response_model=ProductOut, summary="Delete a product", description="Delete a product by ID.")
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    deleted = delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted
