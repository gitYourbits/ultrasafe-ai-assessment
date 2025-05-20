from fastapi import FastAPI
from app.routes import router
import logging
from app.database import SessionLocal, rebuild_faiss_index

app = FastAPI(
    title="Product Catalog API with Semantic Search",
    description="A FastAPI application for managing a product catalog with semantic search capabilities using FAISS and Sentence Transformers.",
    version="1.0.0",
    contact={
        "name": "Your Company",
        "email": "support@example.com",
    },
    openapi_tags=[
        {"name": "products", "description": "Product management and search endpoints."}
    ]
)

@app.on_event("startup")
def on_startup():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("FastAPI application is starting up...")
    # Rebuild FAISS index on startup
    db = SessionLocal()
    rebuild_faiss_index(db)
    db.close()
    logging.info("FAISS index rebuilt on startup.")
    logging.info("API is ready to accept requests.")

@app.get("/", tags=["root"], summary="API Root", description="Welcome message for the Product Catalog API.")
def root():
    return {"message": "Welcome to the Product Catalog API with Semantic Search!"}

app.include_router(router, tags=["products"])
