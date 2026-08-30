"""Self-RAG strategy: decide whether retrieval is needed, retrieve when necessary, inspect answer
grounding.

Simplification note: real Self-RAG (Asai et al., 2023) is trained end-to-end with a model that
emits special "reflection tokens." This implementation approximates the same *behavior* with plain
heuristics/LLM calls instead of a fine-tuned model: an LLM (or, under the mock provider, a keyword
heuristic) decides whether retrieval is needed; grounding is checked via word-overlap between the
answer and retrieved context, not semantic entailment. Documented as an approximation — see
requirement.md's explicit instruction not to claim research-grade Self-RAG.
"""

import re
from collections.abc import Callable

from pydantic import BaseModel

from app.llm.base import LLMMessage, LLMProvider
from app.llm.providers.mock import MockLLMProvider
from app.models.enums import MessageRole
from app.models.rag import RetrievedChunk

_RETRIEVAL_TRIGGER_WORDS = (
    "what",
    "who",
    "when",
    "where",
    "how",
    "which",
    "policy",
    "price",
    "pricing",
    "limit",
    "hours",
    "plan",
)
_WORD_RE = re.compile(r"[a-z0-9]+")


class _RetrievalNeeded(BaseModel):
    retrieval_needed: bool


class SelfRAGResult(BaseModel):
    retrieval_used: bool
    retrieved_context: list[str]
    answer: str
    is_grounded: bool
    grounding_score: float


def word_overlap_ratio(answer: str, context_texts: list[str]) -> float:
    """Fraction of the answer's non-trivial words that also appear in the retrieved context.

    A fast, explainable grounding *proxy* — not semantic entailment. Phase 6 builds a more careful
    (still simplified, still documented) hallucination-detection pipeline on top of this idea.
    """

    answer_words = {w for w in _WORD_RE.findall(answer.lower()) if len(w) > 3}
    if not answer_words:
        return 1.0
    context_words = {w for text in context_texts for w in _WORD_RE.findall(text.lower())}
    if not context_words:
        return 0.0
    return len(answer_words & context_words) / len(answer_words)


class SelfRAGStrategy:
    def __init__(
        self,
        llm: LLMProvider,
        retrieve_fn: Callable[[str], list[RetrievedChunk]],
        generate_fn: Callable[[str, list[str]], str],
        grounding_threshold: float = 0.3,
    ) -> None:
        self._llm = llm
        self._retrieve_fn = retrieve_fn
        self._generate_fn = generate_fn
        self._grounding_threshold = grounding_threshold

    def run(self, query: str) -> SelfRAGResult:
        needs_retrieval = self._needs_retrieval(query)
        context_chunks = self._retrieve_fn(query) if needs_retrieval else []
        context_texts = [c.chunk.content for c in context_chunks]
        answer = self._generate_fn(query, context_texts)
        grounding_score = word_overlap_ratio(answer, context_texts) if context_texts else 1.0
        return SelfRAGResult(
            retrieval_used=needs_retrieval,
            retrieved_context=context_texts,
            answer=answer,
            is_grounded=grounding_score >= self._grounding_threshold,
            grounding_score=grounding_score,
        )

    def _needs_retrieval(self, query: str) -> bool:
        if isinstance(self._llm, MockLLMProvider):
            lowered = query.lower()
            return "?" in query or any(word in lowered for word in _RETRIEVAL_TRIGGER_WORDS)
        decision = self._llm.generate_structured(
            [
                LLMMessage(
                    role=MessageRole.USER,
                    content=(
                        "Does answering this query require looking up specific facts from a "
                        f"knowledge base, as opposed to general conversation? Query: {query}"
                    ),
                )
            ],
            _RetrievalNeeded,
        )
        return decision.retrieval_needed
