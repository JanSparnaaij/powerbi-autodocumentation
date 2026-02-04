"""PBIXRay engine implementation."""

from pathlib import Path
from typing import Any

from ...mcp_client.client import MCPClient
from ...mcp_client.pbixray_tools import PBIXRayClient
from ..base import IDocumentationEngine, ModelMetadata


class PBIXRayEngine(IDocumentationEngine):
    """Documentation engine using pbixray-mcp-server.
    
    This engine supports PBIX files only and uses the pbixray-mcp-server
    for metadata extraction.
    """
    
    def __init__(self, server_script_path: str | None = None):
        """Initialize the PBIXRay engine.
        
        Args:
            server_script_path: Path to pbixray_server.py. Defaults to
                               ./pbixray-mcp-server/src/pbixray_server.py
        """
        if server_script_path is None:
            server_script_path = "./pbixray-mcp-server/src/pbixray_server.py"
        
        self.server_script_path = server_script_path
        self.mcp_client: MCPClient | None = None
        self.pbi_client: PBIXRayClient | None = None
        self._loaded_source: str | None = None
    
    async def load_model(self, source: str, **kwargs) -> None:
        """Load a PBIX file.
        
        Args:
            source: Path to PBIX file
            **kwargs: Ignored for pbixray engine
            
        Raises:
            FileNotFoundError: If PBIX file doesn't exist
            RuntimeError: If pbixray server not found or loading fails
        """
        if not Path(source).exists():
            raise FileNotFoundError(f"PBIX file not found: {source}")
        
        if not Path(self.server_script_path).exists():
            raise RuntimeError(
                f"pbixray-mcp-server not found at {self.server_script_path}"
            )
        
        # Start MCP server
        server_cmd = ["python", self.server_script_path]
        mcp_client_init = MCPClient(server_cmd)
        
        # Connect and initialize client
        self._connection = mcp_client_init.connect()
        self.mcp_client = await self._connection.__aenter__()
        self.pbi_client = PBIXRayClient(self.mcp_client)
        
        # Load the PBIX file
        await self.pbi_client.load_pbix(source)
        self._loaded_source = source
    
    async def extract_metadata(self) -> ModelMetadata:
        """Extract all metadata from the loaded PBIX file.
        
        Returns:
            ModelMetadata: Container with all extracted metadata
            
        Raises:
            RuntimeError: If no model is loaded
        """
        if self.pbi_client is None:
            raise RuntimeError("No model loaded. Call load_model() first.")
        
        # Extract all metadata
        summary = await self.pbi_client.get_model_summary()
        tables = await self.pbi_client.get_tables()
        measures = await self.pbi_client.get_measures()
        relationships = await self.pbi_client.get_relationships()
        
        # Get schema for each table
        for table in tables:
            schema = await self.pbi_client.get_schema(table.name)
            if isinstance(schema, list):
                table.columns = schema
            elif isinstance(schema, dict) and 'columns' in schema:
                table.columns = schema['columns']
        
        # Get Power Query code
        power_query = await self.pbi_client.get_power_query()
        
        return ModelMetadata(
            summary=summary,
            tables=tables,
            measures=measures,
            relationships=relationships,
            power_query={"query": power_query} if power_query else None,
        )
    
    async def close(self) -> None:
        """Close the MCP connection and release resources."""
        if hasattr(self, '_connection') and self._connection is not None:
            await self._connection.__aexit__(None, None, None)
            self.mcp_client = None  # type: ignore
            self.pbi_client = None
            self._loaded_source = None
