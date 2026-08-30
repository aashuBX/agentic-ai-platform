"""Structured (JSON) logging setup.

Kept to the standard library on purpose (Rule 8: minimal dependencies). Phase 8 adds optional
LangSmith/Langfuse exporters on top of the same `AgentEvent` model — this module only owns
process-wide logger configuration and trace-id generation.
"""

import json
import logging
import sys
import uuid
from datetime import UTC, datetime
from typing import Any

_CONFIGURED = False


class JSONFormatter(logging.Formatter):
    """Renders each log record as a single JSON line for easy ingestion/grepping."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        extra = getattr(record, "event_data", None)
        if extra:
            payload.update(extra)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def configure_logging(level: str = "INFO") -> None:
    """Idempotent process-wide logging setup. Safe to call multiple times (e.g. in tests)."""

    global _CONFIGURED
    root = logging.getLogger()
    root.setLevel(level.upper())
    if _CONFIGURED:
        return
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(JSONFormatter())
    root.handlers = [handler]
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def new_trace_id() -> str:
    """Short, URL-safe correlation id attached to every request/workflow run."""

    return uuid.uuid4().hex
