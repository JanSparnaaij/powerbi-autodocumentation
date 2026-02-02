# src/mcp_client/client.py
import asyncio
import json
from contextlib import asynccontextmanager
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """Async client for communicating with MCP servers."""
    
    def __init__(self, server_command: list[str]):
        self.server_params = StdioServerParameters(
            command=server_command[0],
            args=server_command[1:] if len(server_command) > 1 else [],
            env=None
        )
        self.session: ClientSession | None = None
    
    @asynccontextmanager
    async def connect(self):
        """Establish connection to MCP server."""
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self.session = session
                    yield self
                    self.session = None
        except Exception as e:
            raise RuntimeError(f"Failed to connect to MCP server: {e}")
    
    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Call a tool on the MCP server and return the result."""
        if not self.session:
            raise RuntimeError("Not connected to MCP server")
        
        try:
            result = await self.session.call_tool(tool_name, arguments)
            return result
        except Exception as e:
            raise RuntimeError(f"Tool call '{tool_name}' failed: {e}")
    
    async def list_tools(self) -> list[dict]:
        """List all available tools on the MCP server."""
        if not self.session:
            raise RuntimeError("Not connected to MCP server")
        
        try:
            result = await self.session.list_tools()
            return result.tools
        except Exception as e:
            raise RuntimeError(f"Failed to list tools: {e}")
