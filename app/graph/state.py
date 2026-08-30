"""LangGraph conversation state.

A `TypedDict` (not a Pydantic model) on purpose: LangGraph's default reducers merge state updates
key-by-key on plain mappings, which is the best-supported, least surprising option for a first
real workflow. Individual values are still Pydantic models (`ChatMessage`, `IntentClassification`,
`GuardrailReport`) so validation happens wherever it matters — this just avoids fighting LangGraph's
merge semantics with deep Pydantic mutation.

Field list matches requirement.md's LANGGRAPH section exactly. `messages` is the one field with a
non-default reducer (`operator.add`): every other field is "last write wins" per turn — the right
behavior for per-turn scratch state like `intent`/`response`/`guardrail_results` — but `messages`
must *accumulate* across turns of the same session for the LangGraph checkpointer (keyed by
`thread_id = session_id`, see `app/graph/workflow.py`) to provide real short-term memory. Each
`/chat` call feeds in only the one new user message via `new_conversation_state()`; the reducer
appends it to whatever the checkpointer already has for that thread.
"""

import operator
from typing import Annotated, Any, TypedDict

from app.models.enums import GuardrailStatus, IntentCategory, MessageRole
from app.models.guardrails import GuardrailCheckResult, GuardrailReport
from app.models.intent import IntentClassification
from app.models.messages import ChatMessage

# Our own Pydantic models/enums stored directly in ConversationState values. LangGraph's
# checkpoint serializer (JsonPlusSerializer) refuses to deserialize custom types it doesn't
# recognize unless they are explicitly allow-listed — see app/graph/workflow.py, where this list
# configures the checkpointer's serde. Safe to allow-list: these are our own small, controlled
# domain schemas, not attacker-controlled types.
CHECKPOINT_SAFE_TYPES: list[type] = [
    MessageRole,
    ChatMessage,
    IntentCategory,
    IntentClassification,
    GuardrailStatus,
    GuardrailCheckResult,
    GuardrailReport,
]


class ConversationState(TypedDict, total=False):
    session_id: str
    user_id: str | None
    channel: str
    messages: Annotated[list[ChatMessage], operator.add]
    intent: IntentClassification | None
    selected_agent: str | None
    retrieved_context: list[str]
    selected_tools: list[str]
    tool_results: list[dict[str, Any]]
    response: str | None
    guardrail_results: dict[str, GuardrailReport]
    metadata: dict[str, Any]


def new_conversation_state(
    *,
    session_id: str,
    message_text: str,
    trace_id: str,
    channel: str = "web",
    user_id: str | None = None,
) -> ConversationState:
    """Builds the per-turn input fed to `graph.invoke()`.

    `messages` holds only the *new* user message — the `operator.add` reducer appends it to the
    checkpointed history. Every other field is reset for this turn: they are per-turn scratch
    state, not something that should leak from the previous turn.
    """

    return ConversationState(
        session_id=session_id,
        user_id=user_id,
        channel=channel,
        messages=[ChatMessage(role=MessageRole.USER, content=message_text)],
        intent=None,
        selected_agent=None,
        retrieved_context=[],
        selected_tools=[],
        tool_results=[],
        response=None,
        guardrail_results={},
        metadata={"trace_id": trace_id},
    )


def merge_metadata(state: ConversationState, **updates: Any) -> dict[str, Any]:
    """Non-destructively add keys to `state["metadata"]` (LangGraph replaces dict keys wholesale
    on return, so every node that touches metadata must merge explicitly)."""

    return {**state.get("metadata", {}), **updates}
