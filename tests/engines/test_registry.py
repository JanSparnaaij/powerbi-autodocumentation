"""Tests for engine registry and factory."""

import pytest
from src.engines import get_engine, list_engines, register_engine
from src.engines.base import IDocumentationEngine
from src.engines.pbixray import PBIXRayEngine
from src.engines.mcp import ModelingMCPEngine, MCPMode


def test_list_engines():
    """Test listing available engines."""
    engines = list_engines()
    assert "pbixray" in engines
    assert "mcp" in engines
    assert len(engines) >= 2


def test_get_pbixray_engine():
    """Test creating pbixray engine."""
    engine = get_engine("pbixray")
    assert isinstance(engine, PBIXRayEngine)
    assert isinstance(engine, IDocumentationEngine)


def test_get_mcp_engine_default():
    """Test creating MCP engine with default config."""
    engine = get_engine("mcp")
    assert isinstance(engine, ModelingMCPEngine)
    assert isinstance(engine, IDocumentationEngine)
    assert engine.config.mode == MCPMode.READONLY
    assert engine.config.timeout == 60


def test_get_mcp_engine_custom():
    """Test creating MCP engine with custom config."""
    engine = get_engine(
        "mcp",
        server_path="C:\\test\\server.exe",
        mode="readwrite",
        timeout=120,
        max_retries=5
    )
    assert isinstance(engine, ModelingMCPEngine)
    assert engine.config.server_path == "C:\\test\\server.exe"
    assert engine.config.mode == "readwrite"
    assert engine.config.timeout == 120
    assert engine.config.max_retries == 5


def test_get_engine_invalid():
    """Test that invalid engine type raises error."""
    with pytest.raises(ValueError, match="Unknown engine type"):
        get_engine("invalid_engine")


def test_register_custom_engine():
    """Test registering a custom engine."""
    
    class CustomEngine(IDocumentationEngine):
        async def load_model(self, source: str, **kwargs):
            pass
        
        async def extract_metadata(self):
            from src.engines.base import ModelMetadata
            return ModelMetadata(summary={}, tables=[], measures=[], relationships=[])
        
        async def close(self):
            pass
    
    register_engine("custom", CustomEngine)
    
    engines = list_engines()
    assert "custom" in engines
    
    engine = get_engine("custom")
    assert isinstance(engine, CustomEngine)


def test_register_duplicate_engine():
    """Test that registering duplicate engine raises error."""
    with pytest.raises(ValueError, match="already registered"):
        register_engine("pbixray", PBIXRayEngine)
