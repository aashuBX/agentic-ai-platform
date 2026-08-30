"""FAQAgent — answers questions from a small curated FAQ knowledge base.

Phase 1: retrieval is the naive keyword matcher in `app.rag.keyword_search` over
`demo/data/faqs.json`. Generation is grounded — the matched FAQ's canonical answer is passed to
the LLM as context, so answer quality does not depend on the mock provider's (limited) generative
ability. See app/rag/__init__.py for what changes in Phase 2.
"""

from pathlib import Path
from typing import Any

from app.agents.base import BaseAgent
from app.graph.state import ConversationState, merge_metadata
from app.llm.base import LLMMessage
from app.models.agent_config import AgentConfig
from app.models.enums import AgentType, MessageRole
from app.rag.keyword_search import keyword_search, load_knowledge_items

FAQ_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "demo" / "data" / "faqs.json"

_INSTRUCTIONS = (
    "Answer the user's question using only the provided FAQ context. If the context doesn't "
    "actually answer the question, say so plainly instead of guessing."
)

_NO_MATCH_RESPONSE = "I couldn't find a matching FAQ for that question. Try rephrasing, or ask to speak with a human."


class FAQAgent(BaseAgent):
    @classmethod
    def default_config(cls) -> AgentConfig:
        return AgentConfig(
            name="faq_agent",
            agent_type=AgentType.FAQ,
            description="Answers common questions from a curated FAQ knowledge base.",
            instructions=_INSTRUCTIONS,
            knowledge_base=[str(FAQ_DATA_PATH)],
        )

    def _run(self, state: ConversationState) -> dict[str, Any]:
        messages = state.get("messages", [])
        query = next((m.content for m in reversed(messages) if m.role == MessageRole.USER), "")

        items = load_knowledge_items(self.config.knowledge_base[0])
        matches = keyword_search(query, items, top_k=1)

        if not matches:
            return {
                "response": _NO_MATCH_RESPONSE,
                "retrieved_context": [],
                "metadata": merge_metadata(state, faq_match=None),
            }

        item, score = matches[0]
        llm_messages = [
            LLMMessage(role=MessageRole.SYSTEM, content=self.instructions),
            LLMMessage(role=MessageRole.SYSTEM, content=f"CONTEXT: {item.content}"),
            LLMMessage(role=MessageRole.USER, content=query),
        ]
        answer = self.llm.generate(llm_messages)
        return {
            "response": answer.content,
            "retrieved_context": [item.content],
            "metadata": merge_metadata(state, faq_match=item.id, faq_match_score=round(score, 2)),
        }
