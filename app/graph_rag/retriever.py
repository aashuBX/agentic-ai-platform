"""GraphRetriever: relationship-aware retrieval over the knowledge graph.

Finds entities named in the query and returns their outgoing relationships (optionally following
further hops) as `GraphPath`s — this is the "relationship-aware retrieval" requirement.md asks
GraphRAG queries to demonstrate, as opposed to text-similarity search: a query like "Who is the
agent assigned to John Doe?" is answered by graph traversal (Customer --ASSIGNED_TO--> Agent), not
by finding a chunk of text that merely mentions similar words.
"""

import re

from app.graph_rag.repository import GraphRepository
from app.models.graph_rag import GraphEntity, GraphPath

_CAPITALIZED_NAME_RE = re.compile(r"\b[A-Z][a-z]+(?: [A-Z][a-z]+)+\b")


class GraphRetriever:
    def __init__(self, repository: GraphRepository) -> None:
        self._repository = repository

    def retrieve(self, query: str, max_hops: int = 2) -> list[GraphPath]:
        """Finds every capitalized multi-word name in `query` (e.g. "John Doe"), resolves each to
        a known entity, and returns all paths reachable within `max_hops` outgoing relationships.
        """

        candidate_names = _CAPITALIZED_NAME_RE.findall(query)
        paths: list[GraphPath] = []
        seen_start_ids: set[str] = set()
        for name in candidate_names:
            for entity in self._repository.find_entities_by_name(name):
                if entity.id in seen_start_ids:
                    continue
                seen_start_ids.add(entity.id)
                paths.extend(self._expand(entity, max_hops))
        return paths

    def _expand(self, start_entity: GraphEntity, max_hops: int) -> list[GraphPath]:
        paths = [GraphPath(start_entity=start_entity, hops=[])]
        frontier: list[tuple[GraphEntity, list]] = [(start_entity, [])]

        for _ in range(max_hops):
            next_frontier: list[tuple[GraphEntity, list]] = []
            for current_entity, hops_so_far in frontier:
                for relationship, target in self._repository.outgoing(current_entity.id):
                    new_hops = [*hops_so_far, (relationship, target)]
                    paths.append(GraphPath(start_entity=start_entity, hops=new_hops))
                    next_frontier.append((target, new_hops))
            frontier = next_frontier

        return paths
