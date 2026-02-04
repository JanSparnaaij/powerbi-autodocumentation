"""Engine registry and factory for documentation engines.

This module provides a registry pattern for managing and creating documentation
engines dynamically based on engine type.
"""

import logging
from typing import Any

from .base import IDocumentationEngine
from .pbixray import PBIXRayEngine
from .mcp import ModelingMCPEngine, MCPEngineConfig


logger = logging.getLogger(__name__)


# Engine registry
_ENGINE_REGISTRY: dict[str, type[IDocumentationEngine]] = {
    "pbixray": PBIXRayEngine,
    "mcp": ModelingMCPEngine,
}


def register_engine(name: str, engine_class: type[IDocumentationEngine]) -> None:
    """Register a new documentation engine.
    
    Args:
        name: Engine identifier (e.g., "pbixray", "mcp")
        engine_class: Engine class implementing IDocumentationEngine
        
    Raises:
        ValueError: If engine name already registered
    """
    if name in _ENGINE_REGISTRY:
        raise ValueError(f"Engine '{name}' is already registered")
    
    _ENGINE_REGISTRY[name] = engine_class
    logger.info(f"Registered engine: {name}")


def list_engines() -> list[str]:
    """List all registered engine names.
    
    Returns:
        List of engine identifiers
    """
    return list(_ENGINE_REGISTRY.keys())


def get_engine(
    engine_type: str = "pbixray",
    **engine_kwargs: Any
) -> IDocumentationEngine:
    """Create a documentation engine instance.
    
    Args:
        engine_type: Engine identifier (default: "pbixray")
        **engine_kwargs: Engine-specific initialization parameters
            
            For "pbixray":
                - server_script_path: Path to pbixray_server.py
            
            For "mcp":
                - server_path: Path to PowerBI.ModelingMcp.Server.exe
                - mode: Access mode ("readonly" or "readwrite")
                - timeout: Connection timeout in seconds
                - max_retries: Maximum connection retry attempts
                - skip_confirmation: Skip connection confirmation dialogs
                - auto_start: Automatically start the server
    
    Returns:
        Instance of the requested engine
        
    Raises:
        ValueError: If engine type not found
    
    Examples:
        >>> # Use default pbixray engine
        >>> engine = get_engine()
        
        >>> # Use MCP engine with custom config
        >>> engine = get_engine(
        ...     "mcp",
        ...     mode="readonly",
        ...     timeout=120
        ... )
        
        >>> # Use MCP engine with full config
        >>> config = MCPEngineConfig(
        ...     server_path="C:\\path\\to\\PowerBI.ModelingMcp.Server.exe",
        ...     mode=MCPMode.READONLY,
        ...     timeout=60
        ... )
        >>> engine = get_engine("mcp", config=config)
    """
    if engine_type not in _ENGINE_REGISTRY:
        available = ", ".join(list_engines())
        raise ValueError(
            f"Unknown engine type: {engine_type}. "
            f"Available engines: {available}"
        )
    
    engine_class = _ENGINE_REGISTRY[engine_type]
    
    # Handle engine-specific initialization
    if engine_type == "mcp":
        # MCP engine accepts config or individual params
        if "config" in engine_kwargs:
            return engine_class(engine_kwargs["config"])  # type: ignore
        else:
            # Build config from kwargs
            config = MCPEngineConfig(
                server_path=engine_kwargs.get("server_path"),
                mode=engine_kwargs.get("mode", "readonly"),
                timeout=engine_kwargs.get("timeout", 60),
                max_retries=engine_kwargs.get("max_retries", 3),
                skip_confirmation=engine_kwargs.get("skip_confirmation", True),
                auto_start=engine_kwargs.get("auto_start", True),
            )
            return engine_class(config)  # type: ignore
    
    # Default: pass kwargs directly to constructor
    return engine_class(**engine_kwargs)
