"""Entity extraction interface (requirement.md GRAPHRAG section).

`RegexEntityExtractor` is tailored to this repo's synthetic CRM sentence templates (see
`app/graph_rag/seed.py`) — it is a real, working extractor for those specific templates, NOT a
general-purpose NER system, and is documented as such. `LLMEntityExtractor` asks the configured
LLM to extract entities from arbitrary text, which is what a real deployment (fed real documents)
would use; under the mock provider it falls back to the regex extractor rather than trusting the
mock's generic placeholder text as if it were a real extraction.
"""

import re
from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.llm.base import LLMMessage, LLMProvider
from app.llm.providers.mock import MockLLMProvider
from app.models.enums import MessageRole
from app.models.graph_rag import GraphEntity

_NAME = r"[A-Z][\w.'-]*(?: [A-Z][\w.'-]*)*"


def normalize_id(entity_type: str, name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"{entity_type.lower()}:{slug}"


class EntityExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> list[GraphEntity]: ...


_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("Customer", re.compile(rf"^({_NAME}) (?:owns|created|is assigned to|booked)")),
    ("Account", re.compile(r"\baccount (ACCT-\w+)")),
    ("Order", re.compile(r"\border (ORD-\w+)")),
    ("Agent", re.compile(rf"\b(?:agent|with) ({_NAME})")),
    ("Appointment", re.compile(r"\bappointment (APT-\w+)")),
]


class RegexEntityExtractor(EntityExtractor):
    def extract(self, text: str) -> list[GraphEntity]:
        entities: dict[str, GraphEntity] = {}
        for raw_sentence in text.split("."):
            sentence = raw_sentence.strip()
            if not sentence:
                continue
            for entity_type, pattern in _PATTERNS:
                match = pattern.search(sentence)
                if match:
                    name = match.group(1).strip()
                    entity_id = normalize_id(entity_type, name)
                    entities[entity_id] = GraphEntity(
                        id=entity_id, name=name, entity_type=entity_type
                    )
        return list(entities.values())


class _ExtractedEntity(BaseModel):
    name: str
    entity_type: str


class _ExtractedEntityList(BaseModel):
    entities: list[_ExtractedEntity]


class LLMEntityExtractor(EntityExtractor):
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm
        self._fallback = RegexEntityExtractor()

    def extract(self, text: str) -> list[GraphEntity]:
        if isinstance(self._llm, MockLLMProvider):
            return self._fallback.extract(text)

        result = self._llm.generate_structured(
            [
                LLMMessage(
                    role=MessageRole.USER,
                    content=(
                        "Extract every named entity from this text as (name, entity_type) pairs. "
                        "Use entity_type values like Customer, Account, Order, Agent, Appointment "
                        "when they fit; otherwise infer a short PascalCase type.\n\n" + text
                    ),
                )
            ],
            _ExtractedEntityList,
        )
        return [
            GraphEntity(
                id=normalize_id(entity.entity_type, entity.name),
                name=entity.name,
                entity_type=entity.entity_type,
            )
            for entity in result.entities
        ]
