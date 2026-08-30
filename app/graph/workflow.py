"""The first real LangGraph workflow (requirement.md's LANGGRAPH section).

    START -> input_guardrail -[blocked?]-> output_guardrail -> END
                    |
                    v (not blocked)
              intent_agent -> agent_router -[selected_agent]-> {faq, rag, graph_rag, crm, handoff,
                                                                 not_implemented}
                                                                          |
                                                                          v
                                                                  output_guardrail -> END

Uses `add_conditional_edges` twice (blocked-input short-circuit, then agent selection) and
compiles with an in-memory checkpointer keyed by `thread_id = session_id`, giving short-term
cross-turn memory for free. Phase 5 swaps this checkpointer for a Redis-backed one behind the same
`compile(checkpointer=...)` seam — no graph-shape changes needed.

Designed to extend later (per requirement.md) without a rewrite: ReAct-style tool loops and
Plan-and-Execute would add nodes/edges around the existing agent nodes; human approval would add
`interrupt_before=[...]` at compile time; retries are already supported per-node via LangGraph's
`retry_policy` on `add_node`. None of that is implemented yet — noted here so the seam is visible.
"""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.agents.registry import AgentRegistry
from app.graph.nodes import (
    not_implemented_node,
    route_after_input_guardrail,
    route_by_selected_agent,
)
from app.graph.state import CHECKPOINT_SAFE_TYPES, ConversationState

_AGENT_NODES = (
    "faq_agent",
    "rag_agent",
    "graph_rag_agent",
    "crm_agent",
    "handoff_agent",
    "not_implemented",
)


def _new_checkpointer() -> MemorySaver:
    """In-memory checkpointer whose serde explicitly allow-lists our own Pydantic models/enums
    (see CHECKPOINT_SAFE_TYPES) so state round-trips without relying on LangGraph's default
    "warn now, block later" handling of unregistered custom types."""

    serde = JsonPlusSerializer().with_msgpack_allowlist(CHECKPOINT_SAFE_TYPES)
    return MemorySaver(serde=serde)


def build_workflow(registry: AgentRegistry) -> CompiledStateGraph:
    """Builds and compiles the Phase 1 conversational workflow from a shared `AgentRegistry`,
    so the graph and the `/agents` API routes operate on the exact same agent instances."""

    graph = StateGraph(ConversationState)

    graph.add_node("input_guardrail", registry.input_guardrail.execute)
    graph.add_node("intent_agent", registry.intent.execute)
    graph.add_node("agent_router", registry.router.execute)
    graph.add_node("faq_agent", registry.faq.execute)
    graph.add_node("rag_agent", registry.rag.execute)
    graph.add_node("graph_rag_agent", registry.graph_rag.execute)
    graph.add_node("crm_agent", registry.crm.execute)
    graph.add_node("handoff_agent", registry.handoff.execute)
    graph.add_node("not_implemented", not_implemented_node)
    graph.add_node("output_guardrail", registry.output_guardrail.execute)

    graph.add_edge(START, "input_guardrail")
    graph.add_conditional_edges(
        "input_guardrail",
        route_after_input_guardrail,
        {"intent_agent": "intent_agent", "output_guardrail": "output_guardrail"},
    )
    graph.add_edge("intent_agent", "agent_router")
    graph.add_conditional_edges(
        "agent_router",
        route_by_selected_agent,
        {node: node for node in _AGENT_NODES},
    )
    for node in _AGENT_NODES:
        graph.add_edge(node, "output_guardrail")
    graph.add_edge("output_guardrail", END)

    return graph.compile(checkpointer=_new_checkpointer())
