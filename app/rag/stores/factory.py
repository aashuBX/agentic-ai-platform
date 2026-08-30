"""Builds the configured `VectorStore` (`VECTOR_STORE__PROVIDER`, default `chroma`)."""

from app.config.settings import Settings
from app.rag.stores.base import VectorStore

_SUPPORTED = ("chroma", "faiss", "pinecone")


def build_vector_store(settings: Settings, dimension: int) -> VectorStore:
    provider = settings.vector_store.provider.strip().lower()

    if provider == "chroma":
        from app.rag.stores.chroma_store import ChromaVectorStore

        return ChromaVectorStore(
            persist_dir=settings.vector_store.persist_dir,
            collection_name=settings.vector_store.collection_name,
        )
    if provider == "faiss":
        from app.rag.stores.faiss_store import FAISSVectorStore

        return FAISSVectorStore(
            persist_dir=settings.vector_store.persist_dir,
            collection_name=settings.vector_store.collection_name,
            dimension=dimension,
        )
    if provider == "pinecone":
        from app.rag.stores.pinecone_store import PineconeVectorStore

        return PineconeVectorStore(
            api_key=settings.vector_store.pinecone_api_key,
            environment=settings.vector_store.pinecone_environment,
            index_name=settings.vector_store.pinecone_index,
            dimension=dimension,
        )
    raise ValueError(
        f"Unknown VECTOR_STORE__PROVIDER={settings.vector_store.provider!r}. Expected: {_SUPPORTED}"
    )
