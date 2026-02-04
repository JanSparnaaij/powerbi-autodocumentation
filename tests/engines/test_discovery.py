"""Tests for Power BI Modeling MCP server discovery."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from src.engines.mcp.discovery import find_powerbi_mcp_server, validate_server_path


def test_validate_server_path_valid(tmp_path):
    """Test validation of valid server path."""
    # Create a fake executable
    exe_path = tmp_path / "PowerBI.ModelingMcp.Server.exe"
    exe_path.write_text("fake exe")
    
    assert validate_server_path(str(exe_path)) is True


def test_validate_server_path_invalid():
    """Test validation of invalid server path."""
    assert validate_server_path("C:\\nonexistent\\server.exe") is False


def test_validate_server_path_directory(tmp_path):
    """Test that directory path is invalid."""
    assert validate_server_path(str(tmp_path)) is False


@patch.dict(os.environ, {"POWERBI_MCP_PATH": "C:\\test\\server.exe"})
@patch("pathlib.Path.exists")
def test_find_from_env_var_exe(mock_exists):
    """Test finding server from environment variable (exe path)."""
    mock_exists.return_value = True
    
    with patch("pathlib.Path.is_dir", return_value=False):
        with patch("pathlib.Path.name", "PowerBI.ModelingMcp.Server.exe"):
            result = find_powerbi_mcp_server()
            assert result == "C:\\test\\server.exe"


@patch.dict(os.environ, {"POWERBI_MCP_PATH": "C:\\test"})
@patch("pathlib.Path.exists")
@patch("pathlib.Path.is_dir")
def test_find_from_env_var_dir(mock_is_dir, mock_exists):
    """Test finding server from environment variable (directory path)."""
    # Make the directory exist
    mock_exists.side_effect = lambda: True
    mock_is_dir.return_value = True
    
    # Mock the exe inside the directory
    with patch("pathlib.Path.__truediv__") as mock_div:
        exe_path = Path("C:\\test\\PowerBI.ModelingMcp.Server.exe")
        mock_div.return_value = exe_path
        
        with patch.object(Path, "exists", return_value=True):
            result = find_powerbi_mcp_server()
            # Should construct path to exe in directory
            assert result is not None


@patch.dict(os.environ, {}, clear=True)
@patch("platform.system")
def test_find_no_env_var_non_windows(mock_system):
    """Test that non-Windows returns None when no env var set."""
    mock_system.return_value = "Linux"
    
    result = find_powerbi_mcp_server()
    assert result is None


@patch.dict(os.environ, {}, clear=True)
def test_find_returns_none_when_not_found():
    """Test that None is returned when server not found."""
    with patch("platform.system", return_value="Windows"):
        with patch("pathlib.Path.exists", return_value=False):
            result = find_powerbi_mcp_server()
            assert result is None
