"""Query rewriting: asks the LLM to produce a better search query (expand abbreviations, make
implicit references explicit). Under the mock provider this is a documented no-op — it returns
the original query unchanged, since the mock has no real language understanding to rewrite with.
"""

from app.llm.base import LLMMessage, LLMProvider
from app.llm.providers.mock import MockLLMProvider
from app.models.enums import MessageRole

_PROMPT = (
    "Rewrite the following user query to maximize retrieval quality against a knowledge base: "
    "expand abbreviations, make implicit references explicit, keep it a single line, no commentary.\n\n"
    "Query: {query}"
)


class QueryRewriter:
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    def rewrite(self, query: str) -> str:
        if isinstance(self._llm, MockLLMProvider):
            return query
        response = self._llm.generate(
            [LLMMessage(role=MessageRole.USER, content=_PROMPT.format(query=query))]
        )
        rewritten = response.content.strip()
        return rewritten or query
