"""POST /knowledge/search — run the RAG pipeline's retrieval stage directly (no LLM generation),
useful for inspecting/debugging what the hybrid retriever + reranker actually surface.
"""

from fastapi import APIRouter, Depends

from app.api.deps import get_rag_pipeline
from app.models.rag import KnowledgeSearchRequest, KnowledgeSearchResponse, RetrievedChunkView
from app.rag.pipeline import RAGPipeline

router = APIRouter(tags=["knowledge"])


@router.post("/knowledge/search", response_model=KnowledgeSearchResponse)
def search_knowledge(
    request: KnowledgeSearchRequest, pipeline: RAGPipeline = Depends(get_rag_pipeline)
) -> KnowledgeSearchResponse:
    results = pipeline.retrieve(request.query)
    if request.top_k is not None:
        results = results[: request.top_k]
    return KnowledgeSearchResponse(
        query=request.query,
        results=[RetrievedChunkView.from_retrieved_chunk(r) for r in results],
    )
