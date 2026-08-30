"""Agent Runtime / LangGraph workflow layer. See workflow.py for the compiled graph shape.

`build_workflow` is deliberately NOT re-exported here: `app.graph.workflow` imports
`app.agents.registry`, which imports `app.agents.base`, which imports `app.graph.state` — eagerly
importing `workflow` at this package's init time would make that a circular import. Import it
directly: `from app.graph.workflow import build_workflow`.
"""

from app.graph.state import ConversationState, merge_metadata, new_conversation_state

__all__ = ["ConversationState", "merge_metadata", "new_conversation_state"]
