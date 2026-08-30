"""VectorStore interface + Chroma (default)/FAISS/Pinecone(optional) adapters + factory."""

from app.rag.stores.base import VectorStore
from app.rag.stores.factory import build_vector_store

__all__ = ["VectorStore", "build_vector_store"]
