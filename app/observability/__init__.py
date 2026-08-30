"""Observability layer: structured logging, trace IDs, and the agent/tool event bus.

Phase 1 scope: stdlib JSON logging + an in-process `EventBus`. Phase 8 adds optional LangSmith
and Langfuse `EventSink` adapters behind the same interface.
"""

from app.observability.events import (
    AgentEvent,
    EventBus,
    EventSink,
    LoggingEventSink,
    get_event_bus,
)
from app.observability.logging import configure_logging, get_logger, new_trace_id

__all__ = [
    "AgentEvent",
    "EventBus",
    "EventSink",
    "LoggingEventSink",
    "configure_logging",
    "get_event_bus",
    "get_logger",
    "new_trace_id",
]
