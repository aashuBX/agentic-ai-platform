"""Retriever interface — decouples agents from any specific search backend (RULE 4; requirement.md
SEARCH section: "Do not couple the agent directly to a specific database")."""

from abc import ABC, abstractmethod

from app.models.rag import RetrievedChunk


class Retriever(ABC):
    name: str

    @abstractmethod
    def search(self, query: str, top_k: int) -> list[RetrievedChunk]: ...
