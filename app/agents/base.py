"""BaseAgent — the shared abstraction every specialized agent implements.

Per requirement.md's AGENT MODEL section: each agent carries identity/description/instructions/
tools/knowledge sources/configuration/state, exposes one execution method LangGraph can call
directly as a node, and reports through the shared observability event bus (its "logging hooks").
"""

from abc import ABC, abstractmethod
from time import perf_counter
from typing import Any

from app.graph.state import ConversationState, merge_metadata
from app.llm.base import LLMProvider
from app.models.agent_config import AgentConfig
from app.models.enums import AgentType
from app.observability import AgentEvent, get_event_bus, get_logger


class BaseAgent(ABC):
    """Executable, configuration-driven agent.

    Subclasses implement `default_config()` (declarative identity/instructions/connectors/
    knowledge base) and `_run()` (the actual behavior, returning a partial LangGraph state
    update). `execute()` is the LangGraph-callable entry point: it times the run, emits a
    structured event, and guarantees one misbehaving agent cannot crash the whole graph.
    """

    def __init__(self, config: AgentConfig | None = None, llm: LLMProvider | None = None) -> None:
        self.config: AgentConfig = config or self.default_config()
        self.llm = llm
        self.last_run_metadata: dict[str, Any] = {}
        self._logger = get_logger(f"agentic_ai_platform.agents.{self.config.name}")

    @classmethod
    @abstractmethod
    def default_config(cls) -> AgentConfig:
        """Declarative default configuration — what makes this agent configuration-driven."""

    @abstractmethod
    def _run(self, state: ConversationState) -> dict[str, Any]:
        """Subclasses implement the actual behavior and return a partial state update."""

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def description(self) -> str:
        return self.config.description

    @property
    def agent_type(self) -> AgentType:
        return self.config.agent_type

    @property
    def instructions(self) -> str:
        return self.config.instructions

    @property
    def tools(self) -> list[str]:
        return self.config.connectors

    @property
    def knowledge_sources(self) -> list[str]:
        return self.config.knowledge_base

    def execute(self, state: ConversationState) -> dict[str, Any]:
        """LangGraph node entry point. Never raises — a failed agent degrades to an error
        response rather than crashing the whole workflow (ERROR HANDLING section)."""

        trace_id = state.get("metadata", {}).get("trace_id", "unknown")
        start = perf_counter()
        try:
            update = self._run(state)
            status = "success"
        except Exception as exc:  # noqa: BLE001 - one agent's bug must not crash the graph
            self._logger.exception("agent_execution_failed")
            update = {
                "response": f"The {self.name} hit an internal error and could not complete this request.",
                "metadata": merge_metadata(state, error=str(exc), failed_agent=self.name),
            }
            status = "error"

        latency_ms = (perf_counter() - start) * 1000
        self.last_run_metadata = {"status": status, "latency_ms": latency_ms}
        get_event_bus().emit(
            AgentEvent(
                trace_id=trace_id,
                session_id=state.get("session_id"),
                agent=self.name,
                action="execute",
                status=status,
                latency_ms=latency_ms,
            )
        )
        return update
