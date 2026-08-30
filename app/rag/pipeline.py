"""RAGPipeline: orchestrates the full ADVANCED RAG flow end to end.

    DOCUMENT -> PARSER -> HASH -> DEDUPLICATION -> CHUNKING -> EMBEDDING -> VECTOR STORE
    QUERY -> QUERY REWRITER -> {VECTOR SEARCH, BM25 SEARCH} -> RRF -> RERANKER -> CONTEXT

Built from small, independently-testable pieces (parser/dedup/chunker/embedder/store/retrievers/
reranker) — this class just wires them together in the order requirement.md's ADVANCED RAG diagram
specifies. `RAGAgent` calls `retrieve()` and does its own LLM generation with the returned context.
"""

from app.llm.base import LLMProvider
from app.models.rag import Document, IngestResult, RetrievedChunk
from app.rag.chunking.factory import ChunkingFactory
from app.rag.embeddings.base import EmbeddingProvider
from app.rag.ingestion.dedup import Deduplicator
from app.rag.ingestion.parser import DocumentParser
from app.rag.ingestion.repository import RagRepository
from app.rag.reranking.base import Reranker
from app.rag.retrieval.bm25_retriever import BM25Retriever
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.query_rewriter import QueryRewriter
from app.rag.retrieval.vector_retriever import VectorRetriever
from app.rag.stores.base import VectorStore


class RAGPipeline:
    def __init__(
        self,
        repository: RagRepository,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
        llm: LLMProvider,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        chunking_strategy_name: str = "recursive",
        candidate_k: int = 20,
        top_k: int = 5,
        rrf_k: int = 60,
        hybrid_vector_weight: float = 0.5,
        query_rewriting_enabled: bool = False,
        reranker: Reranker | None = None,
    ) -> None:
        self._repository = repository
        self._embedder = embedding_provider
        self._store = vector_store
        self._parser = DocumentParser()
        self._dedup = Deduplicator(repository)
        self._chunking_strategy_name = chunking_strategy_name
        self._chunker = ChunkingFactory.create(
            chunking_strategy_name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            llm=llm,
            embedding_provider=embedding_provider,
        )

        self._bm25 = BM25Retriever()
        self._bm25.index(self._repository.all_chunks())
        self._vector_retriever = VectorRetriever(embedding_provider, vector_store)
        self._hybrid = HybridRetriever(
            self._vector_retriever,
            self._bm25,
            vector_weight=hybrid_vector_weight,
            rrf_k=rrf_k,
            candidate_k=candidate_k,
        )
        self._query_rewriter = QueryRewriter(llm) if query_rewriting_enabled else None
        self._reranker = reranker
        self._candidate_k = candidate_k
        self._top_k = top_k

    def ingest_text(
        self, content: str, *, source: str, title: str, extra_metadata: dict | None = None
    ) -> IngestResult:
        document = self._parser.parse_text(
            content, source=source, title=title, extra_metadata=extra_metadata
        )
        return self._ingest_document(document)

    def ingest_file(
        self,
        file_path: str,
        *,
        source: str | None = None,
        title: str | None = None,
        extra_metadata: dict | None = None,
    ) -> IngestResult:
        document = self._parser.parse_file(
            file_path, source=source, title=title, extra_metadata=extra_metadata
        )
        return self._ingest_document(document)

    def _ingest_document(self, document: Document) -> IngestResult:
        dedup_result = self._dedup.check(document)
        if dedup_result.is_duplicate:
            existing = dedup_result.existing_document
            return IngestResult(
                document_id=existing.id,
                chunk_count=len(self._repository.chunks_for_document(existing.id)),
                was_duplicate=True,
                strategy=self._chunking_strategy_name,
            )

        chunks = self._chunker.chunk(document)
        # LateChunkingStrategy attaches a context-enriched string to embed instead of the raw
        # chunk text (see app/rag/chunking/late.py) — every other strategy leaves this unset, so
        # this is a no-op for them.
        texts_to_embed = [c.metadata.get("embedding_input", c.content) for c in chunks]
        embeddings = self._embedder.embed(texts_to_embed) if chunks else []

        self._repository.save_document(document)
        self._repository.save_chunks(chunks)
        self._store.add(chunks, embeddings)
        self._bm25.index(self._repository.all_chunks())

        return IngestResult(
            document_id=document.id,
            chunk_count=len(chunks),
            was_duplicate=False,
            strategy=self._chunking_strategy_name,
        )

    def retrieve(self, query: str) -> list[RetrievedChunk]:
        search_query = self._query_rewriter.rewrite(query) if self._query_rewriter else query
        fetch_k = self._candidate_k if self._reranker else self._top_k
        candidates = self._hybrid.search(search_query, top_k=fetch_k)
        if self._reranker:
            # Rerank against the ORIGINAL query — the rewrite was only meant to improve search
            # recall, not to redefine what the user actually asked.
            return self._reranker.rerank(query, candidates, top_k=self._top_k)
        return candidates

    def stats(self) -> dict[str, int]:
        return {
            "documents": self._repository.document_count(),
            "chunks": self._repository.chunk_count(),
        }
