"""Non-agent graph nodes and conditional-edge routing functions.

Everything that IS an agent's own behavior lives on that agent's `execute()` method and is
registered directly as a node callable in `workflow.py`. This module only holds the small amount
of glue LangGraph needs that isn't itself an agent: the "not implemented yet" leaf and the two
routing functions.
"""

from typing import Any

from app.agents.router_agent import NOT_IMPLEMENTED_NODE
from app.graph.state import ConversationState, merge_metadata
from app.models.enums import IntentCategory

_PENDING_FEATURE_BY_INTENT: dict[IntentCategory, str] = {
    IntentCategory.FEEDBACK: "the Feedback agent",
    IntentCategory.VOICE_TASK: "voice-specific task handling",
}
_DEFAULT_PENDING_FEATURE = "this capability"


def not_implemented_node(state: ConversationState) -> dict[str, Any]:
    """Honest leaf for intents whose agent doesn't exist in the current phase yet."""

    intent = state.get("intent")
    category = intent.intent if intent else None
    feature = _PENDING_FEATURE_BY_INTENT.get(category, _DEFAULT_PENDING_FEATURE)
    response_text = (
        f"{feature[0].upper()}{feature[1:]} is on this build's roadmap but isn't implemented yet "
        "in the current phase — see PLAN.md for status."
    )
    return {
        "response": response_text,
        "metadata": merge_metadata(state, not_implemented=True, pending_feature=feature),
    }


def route_after_input_guardrail(state: ConversationState) -> str:
    """If the input guardrail blocked the request, skip straight to the output guardrail with
    the rejection message already set, instead of running intent detection on rejected input."""

    report = state.get("guardrail_results", {}).get("input")
    if report is not None and not report.passed:
        return "output_guardrail"
    return "intent_agent"


def route_by_selected_agent(state: ConversationState) -> str:
    """Reads back what `RouterAgent` wrote to `selected_agent`."""

    return state.get("selected_agent") or NOT_IMPLEMENTED_NODE
