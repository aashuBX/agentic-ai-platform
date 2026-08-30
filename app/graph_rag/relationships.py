"""Relationship extraction interface (requirement.md GRAPHRAG section).

`RegexRelationshipExtractor` mirrors `entities.py`'s approach: correct for this repo's fixed
synthetic sentence templates, not a general-purpose relation-extraction system.
"""

import re
from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.graph_rag.entities import normalize_id
from app.llm.base import LLMMessage, LLMProvider
from app.llm.providers.mock import MockLLMProvider
from app.models.enums import MessageRole
from app.models.graph_rag import GraphEntity, GraphRelationship

_NAME = r"[A-Z][\w.'-]*(?: [A-Z][\w.'-]*)*"


class RelationshipExtractor(ABC):
    @abstractmethod
    def extract(self, text: str, entities: list[GraphEntity]) -> list[GraphRelationship]: ...


_PATTERNS: list[tuple[str, str, str, re.Pattern]] = [
    # (relationship_type, source_entity_type, target_entity_type, pattern)
    ("OWNS", "Customer", "Account", re.compile(rf"^({_NAME}) owns account (ACCT-\w+)")),
    ("CREATED", "Customer", "Order", re.compile(rf"^({_NAME}) created order (ORD-\w+)")),
    ("ASSIGNED_TO", "Customer", "Agent", re.compile(rf"^({_NAME}) is assigned to agent ({_NAME})")),
    ("BOOKED", "Customer", "Appointment", re.compile(rf"^({_NAME}) booked appointment (APT-\w+)")),
    ("WITH", "Appointment", "Agent", re.compile(rf"appointment (APT-\w+) with ({_NAME})")),
]


class RegexRelationshipExtractor(RelationshipExtractor):
    def extract(self, text: str, entities: list[GraphEntity]) -> list[GraphRelationship]:
        relationships: list[GraphRelationship] = []
        for raw_sentence in text.split("."):
            sentence = raw_sentence.strip()
            if not sentence:
                continue
            for relationship_type, source_type, target_type, pattern in _PATTERNS:
                match = pattern.search(sentence)
                if not match:
                    continue
                source_id = normalize_id(source_type, match.group(1))
                target_id = normalize_id(target_type, match.group(2))
                relationships.append(
                    GraphRelationship(
                        source_id=source_id,
                        target_id=target_id,
                        relationship_type=relationship_type,
                    )
                )
        return relationships


class _ExtractedRelationship(BaseModel):
    source_id: str
    target_id: str
    relationship_type: str


class _ExtractedRelationshipList(BaseModel):
    relationships: list[_ExtractedRelationship]


class LLMRelationshipExtractor(RelationshipExtractor):
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm
        self._fallback = RegexRelationshipExtractor()

    def extract(self, text: str, entities: list[GraphEntity]) -> list[GraphRelationship]:
        if isinstance(self._llm, MockLLMProvider):
            return self._fallback.extract(text, entities)

        entity_list = "\n".join(f"- {e.id}: {e.name} ({e.entity_type})" for e in entities)
        result = self._llm.generate_structured(
            [
                LLMMessage(
                    role=MessageRole.USER,
                    content=(
                        f"Given these entities:\n{entity_list}\n\n"
                        "Extract every relationship between them expressed in this text. Use each "
                        "entity's id (exactly as given above) as source_id/target_id, and a short "
                        "UPPER_SNAKE_CASE relationship_type.\n\n" + text
                    ),
                )
            ],
            _ExtractedRelationshipList,
        )
        return [
            GraphRelationship(
                source_id=r.source_id, target_id=r.target_id, relationship_type=r.relationship_type
            )
            for r in result.relationships
        ]
