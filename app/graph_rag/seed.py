"""Seeds the knowledge graph from `demo/data/relationships.json`, converting each structured
record into narrative sentences and running them through the real `GraphBuilder` extraction
pipeline — this exercises entity/relationship extraction genuinely, rather than writing graph
nodes/edges directly and skipping the pipeline the rest of this module implements.

Idempotent: `GraphRepository.upsert_entity`/`upsert_relationship` dedupe, so calling this on every
startup is a harmless no-op after the first time (mirrors `app.rag.seed.seed_demo_knowledge`).
"""

import json
from pathlib import Path

from app.graph_rag.builder import GraphBuilder
from app.observability import get_logger

_DEMO_RELATIONSHIPS_PATH = (
    Path(__file__).resolve().parent.parent.parent / "demo" / "data" / "relationships.json"
)
_logger = get_logger("agentic_ai_platform.graph_rag.seed")


def _record_to_sentences(record: dict[str, str]) -> str:
    return (
        f"{record['customer']} owns account {record['account']}. "
        f"{record['customer']} created order {record['order']}. "
        f"{record['customer']} is assigned to agent {record['agent']}. "
        f"{record['customer']} booked appointment {record['appointment']} with {record['agent']}."
    )


def seed_demo_graph(builder: GraphBuilder, path: Path = _DEMO_RELATIONSHIPS_PATH) -> dict[str, int]:
    """Returns total entity/relationship counts extracted (not necessarily newly-added, since
    upserts are idempotent)."""

    if not path.exists():
        return {"entities": 0, "relationships": 0}

    records = json.loads(path.read_text(encoding="utf-8"))
    total_entities = 0
    total_relationships = 0
    for record in records:
        result = builder.build_and_store(_record_to_sentences(record))
        total_entities += len(result.entities)
        total_relationships += len(result.relationships)

    _logger.info(
        "demo_graph_seeded",
        extra={
            "event_data": {
                "records": len(records),
                "entities_extracted": total_entities,
                "relationships_extracted": total_relationships,
            }
        },
    )
    return {"entities": total_entities, "relationships": total_relationships}
