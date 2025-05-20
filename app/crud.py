from sqlalchemy.orm import Session
from app.models import ProductORM
from app.schemas import ProductCreate, ProductUpdate
from app.database import add_product_embedding, update_product_embedding, delete_product_embedding

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ProductORM).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(ProductORM).filter(ProductORM.id == product_id).first()

def create_product(db: Session, product: ProductCreate):
    db_product = ProductORM(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    add_product_embedding(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    update_product_embedding(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()
    delete_product_embedding(product_id)
    return db_product
