import pandas as pd
from sqlalchemy.orm import Session
from app.models import ProductORM, Base
from app.database import SessionLocal, engine, rebuild_faiss_index
import argparse
import os
import logging

def load_data(force=False):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Ensuring tables exist and loading product data...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()

    # Check if data already exists
    if not force and db.query(ProductORM).first():
        logging.info("Data already loaded. Aborting.")
        db.close()
        return

    # Use absolute path to products.csv for reliability
    csv_path = os.path.join(os.path.dirname(__file__), 'products.csv')
    df = pd.read_csv(csv_path)

    products = []
    for _, row in df.iterrows():
        product = ProductORM(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            price=row["price"],
            categories=row["categories"],
            rating=row["rating"],
            brand=row["brand"]
        )
        products.append(product)

    db.add_all(products)
    db.commit()
    # Rebuild FAISS index after loading data
    rebuild_faiss_index(db)
    db.close()

    logging.info(f"{len(products)} products loaded into the database and FAISS index rebuilt.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Force reload of data.")
    args = parser.parse_args()

    load_data(force=args.force)
