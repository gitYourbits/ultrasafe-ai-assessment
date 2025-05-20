# Product Catalog API with Semantic Search

A production-ready FastAPI application for managing a product catalog with advanced semantic search capabilities using FAISS and Sentence Transformers.

---

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup & Data Loading](#setup--data-loading)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Semantic Search & RAG Design](#semantic-search--rag-design)
- [Error Handling & Validation](#error-handling--validation)
- [Performance & Caching](#performance--caching)
- [Extending & Customization](#extending--customization)
- [License](#license)

---

## Features
- CRUD API for products (Create, Read, Update, Delete)
- Semantic Search endpoint using FAISS and Sentence Transformers
- Vector database integration for fast similarity search
- Automatic embedding updates on product add/update/delete
- Robust error handling and validation
- Modular, production-grade codebase

---

## Requirements
- Python 3.8+
- All dependencies are listed in `requirements.txt` (FastAPI, SQLAlchemy, FAISS, sentence-transformers, etc.)

---

## Installation
1. The repository should be cloned:
   ```bash
   git clone <your-repo-url>
   cd ultrasafeai
   ```
2. A virtual environment is recommended and can be created as follows:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Dependencies are installed with:
   ```bash
   pip install -r requirements.txt
   ```

---

## Setup & Data Loading
1. The database and product data are prepared as follows:
   - The `products.csv` file should be placed in the `app/` directory (already present by default).
   - The data loader is executed:
     ```bash
     python app/utils.py --force    # force argument not required if loading the data first time
     ```
   - This command creates the SQLite database, loads all products, and builds the FAISS index for semantic search.

2. (Optional) If `products.csv` is updated, the above command can be rerun with `--force` to reload and re-index the data.

---

## Running the Application
The FastAPI server is started with:
```bash
uvicorn app.main:app --reload
```
- The API will be available at `http://127.0.0.1:8000/`
- Interactive API documentation is provided at `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Product Management
- `GET /products` — Lists all products (with pagination)
- `GET /products/{id}` — Retrieves product details by ID
- `POST /products` — Adds a new product
- `PUT /products/{id}` — Updates a product
- `DELETE /products/{id}` — Deletes a product

### Semantic Search
- `GET /products/search?q=QUERY&top_k=5` — Performs semantic search for products using a query string
  - Returns the most semantically similar products to the query

### Root
- `GET /` — Returns a welcome message

All endpoints are documented in the OpenAPI documentation (`/docs`).

---

## Semantic Search & RAG Design

### How Semantic Search Works
- Product data (name, description, categories, brand) is embedded using a transformer model (`all-MiniLM-L6-v2`).
- Embeddings are indexed in FAISS for fast vector similarity search.
- The `/products/search` endpoint embeds the query and retrieves the most similar products.
- The FAISS index is always kept in sync with the database (on startup, data load, add/update/delete).

### RAG (Retrieval-Augmented Generation) Pipeline
- **Retrieval:** The semantic search endpoint retrieves the most relevant products for a given query using dense vector similarity.
- **Augmentation:** The retrieved product data can be used to augment queries or as context for downstream tasks (e.g., recommendations, chatbots, or generative models).
- **Generation:** While this API does not generate new text, it provides the retrieval backbone for a RAG system. The system can be extended to generate answers or recommendations based on retrieved products using LLMs or other generative models.
- **Design Choices:**
  - FAISS is used for scalable, efficient vector search
  - Sentence Transformers are used for high-quality semantic embeddings
  - FastAPI is used for modern, robust API development

---

## Error Handling & Validation
- All endpoints use Pydantic models for request/response validation.
- 404 errors are returned for missing products, 422 for validation errors, and clear error messages are provided for all failure cases.

---

## Performance & Caching
- The FAISS in-memory index provides fast semantic search out of the box.
- Explicit caching (e.g., Redis, in-memory cache) is not included by default, as FAISS already ensures sub-millisecond search for most use cases.
- Explicit caching may be considered if extremely high read traffic is expected, or if expensive DB queries or API responses need to be cached (e.g., using `fastapi-cache2`, Redis, or similar).
- For most deployments, explicit caching is not required unless performance bottlenecks are observed under load.

---

## Extending & Customization
- The embedding model can be swapped for a domain-specific one if needed.
- Integration with other vector DBs (e.g., Pinecone, Weaviate) can be achieved by adapting the vector search logic.
- Authentication, rate limiting, or monitoring can be added as needed for the deployment environment.
- The RAG pipeline can be extended with a generative model for Q&A or recommendations.
