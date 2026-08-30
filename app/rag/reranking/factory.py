"""Builds the configured `Reranker` (`RAG__RERANKER`: none | cross_encoder | llm)."""

from app.config.settings import RAGSettings
from app.llm.base import LLMProvider
from app.rag.reranking.base import Reranker

_SUPPORTED = ("none", "cross_encoder", "llm")


def build_reranker(rag_settings: RAGSettings, llm: LLMProvider) -> Reranker | None:
    choice = rag_settings.reranker.strip().lower()

    if choice == "none":
        return None
    if choice == "cross_encoder":
        from app.rag.reranking.cross_encoder import CrossEncoderReranker

        return CrossEncoderReranker(model_name=rag_settings.reranker_model)
    if choice == "llm":
        from app.rag.reranking.llm_reranker import LLMReranker

        return LLMReranker(llm=llm)

    raise ValueError(
        f"Unknown RAG__RERANKER={rag_settings.reranker!r}. Expected one of: {_SUPPORTED}"
    )
