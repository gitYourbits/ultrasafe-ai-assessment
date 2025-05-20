import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import ProductORM, Base
import logging
from tqdm import tqdm

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

logging.info("Loading embedding model 'all-MiniLM-L6-v2'...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
logging.info("Embedding model loaded successfully.")

faiss_index = None
product_id_map = []  # Maps FAISS index to product IDs


def get_embedding(text: str):
    return embedding_model.encode(text, normalize_embeddings=True)


def product_to_text(product):
    # Use all relevant fields for embedding, handle None gracefully
    return f"{product.name} {product.description} {product.categories or ''} {product.brand or ''}"


def rebuild_faiss_index(db):
    global faiss_index, product_id_map
    logging.info("Rebuilding FAISS index from database...")
    products = db.query(ProductORM).all()
    embeddings = []
    for p in tqdm(products, desc="Generating embeddings", unit="product"):
        embeddings.append(get_embedding(product_to_text(p)))
    if embeddings:
        dim = len(embeddings[0])
        faiss_index = faiss.IndexFlatL2(dim)
        faiss_index.add(np.array(embeddings).astype('float32'))
        product_id_map = [p.id for p in products]
        logging.info(f"FAISS index built with {len(embeddings)} products.")
    else:
        faiss_index = None
        product_id_map = []
        logging.info("FAISS index cleared (no products found).")


def add_product_embedding(product):
    global faiss_index, product_id_map
    logging.info(f"Adding embedding for product id={product.id}...")
    embed = get_embedding(product_to_text(product))
    if faiss_index is None:
        dim = len(embed)
        faiss_index = faiss.IndexFlatL2(dim)
        faiss_index.add(np.array([embed]).astype('float32'))
        product_id_map.append(product.id)
    else:
        faiss_index.add(np.array([embed]).astype('float32'))
        product_id_map.append(product.id)
    logging.info(f"Embedding added for product id={product.id}.")


def update_product_embedding(product):
    logging.info(f"Updating embedding for product id={product.id} (rebuilding index)...")
    db = SessionLocal()
    rebuild_faiss_index(db)
    db.close()
    logging.info(f"Embedding updated for product id={product.id}.")


def delete_product_embedding(product_id):
    logging.info(f"Deleting embedding for product id={product_id} (rebuilding index)...")
    db = SessionLocal()
    rebuild_faiss_index(db)
    db.close()
    logging.info(f"Embedding deleted for product id={product_id}.")


def semantic_search(query: str, top_k: int = 5):
    global faiss_index, product_id_map
    logging.info(f"Performing semantic search for query: '{query}' (top_k={top_k})...")
    if not faiss_index or not product_id_map:
        logging.info("No FAISS index or product embeddings available for search.")
        return []
    query_vec = get_embedding(query).astype('float32').reshape(1, -1)
    D, I = faiss_index.search(query_vec, top_k)
    matched_ids = [product_id_map[idx] for idx in I[0] if idx < len(product_id_map)]
    logging.info(f"Semantic search returned {len(matched_ids)} results.")
    return matched_ids
