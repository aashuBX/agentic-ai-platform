"""Structured agent/tool execution events.

`AgentEvent` matches the shape from requirement.md's OBSERVABILITY section. `EventSink` is the
extension point Rule 4 asks for: Phase 1 ships only `LoggingEventSink` (stdlib logging); Phase 8
adds `LangSmithEventSink` / `LangfuseEventSink` behind the same interface, enabled purely via
config, with no changes to call sites.
"""

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from app.observability.logging import get_logger

_logger = get_logger("agentic_ai_platform.events")


class AgentEvent(BaseModel):
    """One structured, loggable fact about something the platform did."""

    trace_id: str
    session_id: str | None = None
    agent: str
    action: str
    tool: str | None = None
    status: str = "success"
    latency_ms: float | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    extra: dict[str, Any] = Field(default_factory=dict)


class EventSink(ABC):
    """Where events go. Implement this to add a new observability backend."""

    @abstractmethod
    def emit(self, event: AgentEvent) -> None: ...


class LoggingEventSink(EventSink):
    """Default sink: one structured JSON log line per event. Always active, zero dependencies."""

    def emit(self, event: AgentEvent) -> None:
        _logger.info(
            "agent_event",
            extra={"event_data": event.model_dump(mode="json")},
        )


class EventBus:
    """Fan-out dispatcher over one or more sinks. Sinks are registered at process startup."""

    def __init__(self, sinks: list[EventSink] | None = None) -> None:
        self._sinks: list[EventSink] = sinks or [LoggingEventSink()]

    def register(self, sink: EventSink) -> None:
        self._sinks.append(sink)

    def emit(self, event: AgentEvent) -> None:
        for sink in self._sinks:
            # A misbehaving observability sink must never break the request it is observing.
            try:
                sink.emit(event)
            except Exception:  # noqa: BLE001
                _logger.exception(
                    "event_sink_failed", extra={"event_data": {"sink": type(sink).__name__}}
                )


_event_bus = EventBus()


def get_event_bus() -> EventBus:
    return _event_bus
