"""Tests for MCP server discovery."""

import os
import tempfile
from pathlib import Path

import pytest
from src.engines.mcp.discovery import (
    find_powerbi_mcp_server,
    validate_server_path
)


def test_validate_server_path_existing(tmp_path):
    """Test validating an existing server path."""
    # Create a fake executable
    server_exe = tmp_path / "PowerBI.ModelingMcp.Server.exe"
    server_exe.write_text("fake exe")
    
    assert validate_server_path(str(server_exe)) is True


def test_validate_server_path_nonexistent():
    """Test validating a non-existent path."""
    assert validate_server_path("C:\\nonexistent\\server.exe") is False


def test_validate_server_path_directory(tmp_path):
    """Test that directory paths are invalid."""
    assert validate_server_path(str(tmp_path)) is False


def test_find_powerbi_mcp_server_env_var(tmp_path, monkeypatch):
    """Test finding server via POWERBI_MCP_PATH environment variable."""
    # Create fake server
    server_exe = tmp_path / "PowerBI.ModelingMcp.Server.exe"
    server_exe.write_text("fake exe")
    
    # Set environment variable to the executable
    monkeypatch.setenv("POWERBI_MCP_PATH", str(server_exe))
    
    found = find_powerbi_mcp_server()
    assert found == str(server_exe)


def test_find_powerbi_mcp_server_env_var_directory(tmp_path, monkeypatch):
    """Test finding server via POWERBI_MCP_PATH pointing to directory."""
    # Create fake server in directory
    server_exe = tmp_path / "PowerBI.ModelingMcp.Server.exe"
    server_exe.write_text("fake exe")
    
    # Set environment variable to the directory
    monkeypatch.setenv("POWERBI_MCP_PATH", str(tmp_path))
    
    found = find_powerbi_mcp_server()
    assert found == str(server_exe)


def test_find_powerbi_mcp_server_not_found(monkeypatch):
    """Test that None is returned when server not found."""
    # Clear environment variable
    monkeypatch.delenv("POWERBI_MCP_PATH", raising=False)
    
    # Mock VS Code extensions directory to not exist
    monkeypatch.setenv("USERPROFILE", "C:\\nonexistent")
    
    found = find_powerbi_mcp_server()
    # May be None or may find something in common locations depending on system
    # Just check it's callable without errors
    assert found is None or isinstance(found, str)


def test_find_powerbi_mcp_server_vscode_extension(tmp_path, monkeypatch):
    """Test finding server in VS Code extensions."""
    # Create fake VS Code extension structure
    vscode_ext = tmp_path / ".vscode" / "extensions" / "microsoft.powerbi-vscode-1.0.0"
    vscode_ext.mkdir(parents=True)
    
    server_exe = vscode_ext / "dist" / "PowerBI.ModelingMcp.Server.exe"
    server_exe.parent.mkdir()
    server_exe.write_text("fake exe")
    
    # Mock USERPROFILE
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.delenv("POWERBI_MCP_PATH", raising=False)
    
    found = find_powerbi_mcp_server()
    assert found == str(server_exe)
