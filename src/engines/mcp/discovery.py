"""Power BI Modeling MCP Server discovery utilities.

This module handles auto-discovery of the Power BI Modeling MCP Server executable
from various installation locations.
"""

import os
import platform
from pathlib import Path


def find_powerbi_mcp_server() -> str | None:
    """Find the Power BI Modeling MCP Server executable.
    
    Search order:
    1. POWERBI_MCP_PATH environment variable
    2. VS Code extension installation path
    3. Common installation directories
    
    Returns:
        Path to PowerBI.ModelingMcp.Server.exe or None if not found
    """
    # 1. Check environment variable
    env_path = os.getenv("POWERBI_MCP_PATH")
    if env_path:
        path = Path(env_path)
        if path.exists():
            # If it's a directory, look for the executable
            if path.is_dir():
                exe = path / "PowerBI.ModelingMcp.Server.exe"
                if exe.exists():
                    return str(exe)
            # If it's already the executable
            elif path.name.endswith(".exe"):
                return str(path)
    
    # 2. Check VS Code extensions
    if platform.system() == "Windows":
        user_profile = os.getenv("USERPROFILE")
        if user_profile:
            vscode_extensions = Path(user_profile) / ".vscode" / "extensions"
            if vscode_extensions.exists():
                # Look for Microsoft Power BI extension
                for ext_dir in vscode_extensions.iterdir():
                    if "microsoft.powerbi-vscode" in ext_dir.name.lower():
                        # Check common subpaths
                        possible_paths = [
                            ext_dir / "dist" / "PowerBI.ModelingMcp.Server.exe",
                            ext_dir / "bin" / "PowerBI.ModelingMcp.Server.exe",
                            ext_dir / "PowerBI.ModelingMcp.Server.exe",
                        ]
                        for exe_path in possible_paths:
                            if exe_path.exists():
                                return str(exe_path)
    
    # 3. Check common installation directories (Windows)
    if platform.system() == "Windows":
        common_paths = [
            Path(os.getenv("ProgramFiles", "C:\\Program Files")) / "Microsoft" / "Power BI Desktop" / "bin" / "PowerBI.ModelingMcp.Server.exe",
            Path(os.getenv("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "Microsoft" / "Power BI Desktop" / "bin" / "PowerBI.ModelingMcp.Server.exe",
            Path(os.getenv("LOCALAPPDATA", "")) / "Microsoft" / "PowerBI Desktop" / "PowerBI.ModelingMcp.Server.exe",
        ]
        for path in common_paths:
            if path.exists():
                return str(path)
    
    return None


def validate_server_path(server_path: str) -> bool:
    """Validate that the server path exists and is executable.
    
    Args:
        server_path: Path to the server executable
        
    Returns:
        True if valid, False otherwise
    """
    path = Path(server_path)
    return path.exists() and path.is_file()
