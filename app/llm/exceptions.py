"""LLM-layer exceptions. Callers (agents, graph nodes) catch `LLMError` and degrade gracefully
rather than letting a provider failure crash the workflow (requirement.md's ERROR HANDLING section).
"""


class LLMError(Exception):
    """Base class for all LLM provider errors."""


class ProviderNotConfiguredError(LLMError):
    """Provider selected via config but missing its SDK extra or API key.

    Raised at provider-construction time with a message telling the operator exactly which
    extra to install / which env var to set — never silently falls back to another provider,
    per RULE 1 (never invent that a provider is working).
    """


class StructuredOutputError(LLMError):
    """`generate_structured()` could not obtain schema-valid JSON after all retries."""


class LLMTimeoutError(LLMError):
    """A provider call exceeded its configured timeout."""
