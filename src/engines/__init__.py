"""Documentation engine abstraction layer for Power BI models.

This module provides a pluggable engine architecture to support multiple
Power BI documentation backends (pbixray, Power BI Modeling MCP Server, etc.).
"""

from .base import IDocumentationEngine, ModelMetadata
from .registry import get_engine, register_engine, list_engines

__all__ = [
    "IDocumentationEngine",
    "ModelMetadata",
    "get_engine",
    "register_engine",
    "list_engines",
]
