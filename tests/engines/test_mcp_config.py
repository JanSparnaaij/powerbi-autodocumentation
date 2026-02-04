"""Tests for MCP engine configuration."""

import pytest
from src.engines.mcp.config import MCPEngineConfig, MCPMode


def test_mcp_config_defaults():
    """Test default MCP configuration."""
    config = MCPEngineConfig()
    
    assert config.server_path is None
    assert config.mode == MCPMode.READONLY
    assert config.timeout == 60
    assert config.max_retries == 3
    assert config.skip_confirmation is True
    assert config.auto_start is True


def test_mcp_config_custom():
    """Test custom MCP configuration."""
    config = MCPEngineConfig(
        server_path="C:\\test\\server.exe",
        mode=MCPMode.READWRITE,
        timeout=120,
        max_retries=5,
        skip_confirmation=False,
        auto_start=False
    )
    
    assert config.server_path == "C:\\test\\server.exe"
    assert config.mode == MCPMode.READWRITE
    assert config.timeout == 120
    assert config.max_retries == 5
    assert config.skip_confirmation is False
    assert config.auto_start is False


def test_get_server_args_readonly():
    """Test server args for readonly mode."""
    config = MCPEngineConfig(mode=MCPMode.READONLY)
    args = config.get_server_args()
    
    assert "--start" in args
    assert "--skipconfirmation" in args
    assert "--readonly" in args
    assert "--readwrite" not in args


def test_get_server_args_readwrite():
    """Test server args for readwrite mode."""
    config = MCPEngineConfig(mode=MCPMode.READWRITE)
    args = config.get_server_args()
    
    assert "--start" in args
    assert "--skipconfirmation" in args
    assert "--readwrite" in args
    assert "--readonly" not in args


def test_get_server_args_no_start():
    """Test server args without auto-start."""
    config = MCPEngineConfig(auto_start=False, skip_confirmation=False)
    args = config.get_server_args()
    
    assert "--start" not in args
    assert "--skipconfirmation" not in args
    assert "--readonly" in args


def test_mcp_mode_enum():
    """Test MCPMode enum values."""
    assert MCPMode.READONLY.value == "readonly"
    assert MCPMode.READWRITE.value == "readwrite"
    
    # Test string conversion
    assert MCPMode("readonly") == MCPMode.READONLY
    assert MCPMode("readwrite") == MCPMode.READWRITE
