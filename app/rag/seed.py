"""Seeds the RAG pipeline with the demo knowledge documents at startup, so a fresh clone has real
content to retrieve against (requirement.md SUCCESS CRITERIA #9: "execute an RAG query"). Ingestion
dedups by content hash, so calling this on every startup is a harmless no-op after the first time.
"""

import json
from pathlib import Path

from app.observability import get_logger
from app.rag.pipeline import RAGPipeline

_DEMO_KNOWLEDGE_PATH = (
    Path(__file__).resolve().parent.parent.parent / "demo" / "data" / "knowledge_documents.json"
)
_logger = get_logger("agentic_ai_platform.rag.seed")


def seed_demo_knowledge(pipeline: RAGPipeline, path: Path = _DEMO_KNOWLEDGE_PATH) -> int:
    """Returns the number of documents newly ingested (0 if already seeded or the file is missing)."""

    if not path.exists():
        return 0

    documents = json.loads(path.read_text(encoding="utf-8"))
    newly_ingested = 0
    for document in documents:
        result = pipeline.ingest_text(
            document["content"], source=document["id"], title=document["title"]
        )
        if not result.was_duplicate:
            newly_ingested += 1

    _logger.info(
        "demo_knowledge_seeded",
        extra={"event_data": {"new_documents": newly_ingested, "total_documents": len(documents)}},
    )
    return newly_ingested
