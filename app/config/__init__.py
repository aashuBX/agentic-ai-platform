"""Configuration layer: a single `Settings` object, grouped by integration category.

Import `get_settings()` rather than constructing `Settings()` directly so the whole process
shares one cached, validated configuration snapshot.
"""

from app.config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
