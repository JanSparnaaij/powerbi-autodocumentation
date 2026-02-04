"""Configuration for Power BI Modeling MCP engine."""

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class MCPMode(str, Enum):
    """MCP server access mode."""
    READONLY = "readonly"
    READWRITE = "readwrite"


@dataclass
class MCPEngineConfig:
    """Configuration for Power BI Modeling MCP engine.
    
    Attributes:
        server_path: Path to PowerBI.ModelingMcp.Server.exe (auto-discovered if None)
        mode: Access mode (readonly or readwrite). Defaults to readonly.
        timeout: Connection timeout in seconds. Defaults to 60.
        max_retries: Maximum connection retry attempts. Defaults to 3.
        skip_confirmation: Skip connection confirmation dialogs. Defaults to True.
        auto_start: Automatically start the server. Defaults to True.
    """
    
    server_path: str | None = None
    mode: MCPMode = MCPMode.READONLY
    timeout: int = 60
    max_retries: int = 3
    skip_confirmation: bool = True
    auto_start: bool = True
    
    def get_server_args(self) -> list[str]:
        """Get command-line arguments for the MCP server.
        
        Returns:
            List of command-line arguments
        """
        args = []
        
        if self.auto_start:
            args.append("--start")
        
        if self.skip_confirmation:
            args.append("--skipconfirmation")
        
        if self.mode == MCPMode.READWRITE:
            args.append("--readwrite")
        else:
            args.append("--readonly")
        
        return args
