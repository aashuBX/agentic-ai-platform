"""Retriever interface + vector/BM25/hybrid(+RRF) implementations, query rewriting, and the
Self-RAG / CRAG strategy modules."""

from app.rag.retrieval.base import Retriever
from app.rag.retrieval.bm25_retriever import BM25Retriever
from app.rag.retrieval.crag import CRAGResult, CRAGStrategy
from app.rag.retrieval.hybrid_retriever import HybridRetriever, reciprocal_rank_fusion
from app.rag.retrieval.query_rewriter import QueryRewriter
from app.rag.retrieval.self_rag import SelfRAGResult, SelfRAGStrategy
from app.rag.retrieval.vector_retriever import VectorRetriever

__all__ = [
    "BM25Retriever",
    "CRAGResult",
    "CRAGStrategy",
    "HybridRetriever",
    "QueryRewriter",
    "Retriever",
    "SelfRAGResult",
    "SelfRAGStrategy",
    "VectorRetriever",
    "reciprocal_rank_fusion",
]
