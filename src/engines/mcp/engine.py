"""Power BI Modeling MCP engine implementation.

This engine uses the Microsoft Power BI Modeling MCP Server to extract metadata
from Power BI models. It supports PBIP folders, TMDL format, and live connections
to Power BI Desktop.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from ...mcp_client.client import MCPClient
from ...mcp_client.pbixray_tools import Table, Measure, Relationship
from ..base import IDocumentationEngine, ModelMetadata
from .config import MCPEngineConfig, MCPMode
from .discovery import find_powerbi_mcp_server, validate_server_path


logger = logging.getLogger(__name__)


def _parse_mcp_result(result) -> dict[str, Any]:
    """Parse MCP CallToolResult into dictionary.
    
    Args:
        result: CallToolResult from MCP session.call_tool()
        
    Returns:
        Parsed JSON data from the result
    """
    if hasattr(result, 'content') and result.content:
        # Result is a CallToolResult with content list
        for content_item in result.content:
            if hasattr(content_item, 'text'):
                # Parse JSON from text content
                return json.loads(content_item.text)
    
    # Fallback: treat as dict
    if isinstance(result, dict):
        return result
    
    logger.warning(f"Unexpected result type: {type(result)}")
    return {}


class ModelingMCPEngine(IDocumentationEngine):
    """Documentation engine using Power BI Modeling MCP Server.
    
    This engine supports:
    - PBIP folders (TMDL format)
    - Power BI Desktop live connections
    - Analysis Services connections
    - Read-only and read-write modes
    """
    
    def __init__(self, config: MCPEngineConfig | None = None):
        """Initialize the Modeling MCP engine.
        
        Args:
            config: Engine configuration. Auto-discovers server if not provided.
        """
        self.config = config or MCPEngineConfig()
        self.mcp_client: MCPClient
        self._connection = None  # Store the connection context manager
        self._loaded_source: str | None = None
        self._connection_id: str | None = None
        self._available_tools: set[str] = set()
    
    async def load_model(self, source: str, **kwargs) -> None:
        """Load a Power BI model.
        
        Supports multiple source types:
        - PBIP folder path
        - Power BI Desktop connection string (powerbi://...)
        - XMLA endpoint connection string
        
        Args:
            source: Model source (PBIP folder, connection string, etc.)
            **kwargs: Additional options:
                - mode: Override config mode (readonly/readwrite)
                - timeout: Override config timeout
                
        Raises:
            FileNotFoundError: If PBIP folder doesn't exist
            RuntimeError: If server not found or connection fails
        """
        # Discover server if not configured
        if self.config.server_path is None:
            server_path = find_powerbi_mcp_server()
            if server_path is None:
                raise RuntimeError(
                    "Power BI Modeling MCP Server not found. "
                    "Set POWERBI_MCP_PATH environment variable or install "
                    "the Power BI VS Code extension."
                )
            self.config.server_path = server_path
            logger.info(f"Auto-discovered MCP server: {server_path}")
        
        if not validate_server_path(self.config.server_path):
            raise RuntimeError(
                f"Invalid MCP server path: {self.config.server_path}"
            )
        
        # Override config from kwargs
        if "mode" in kwargs:
            mode_str = kwargs["mode"]
            self.config.mode = MCPMode(mode_str)
        
        if "timeout" in kwargs:
            self.config.timeout = int(kwargs["timeout"])
        
        # Build server command
        server_cmd = [self.config.server_path] + self.config.get_server_args()
        logger.info(f"Starting MCP server: {' '.join(server_cmd)}")
        
        # Start MCP server with retries
        for attempt in range(self.config.max_retries):
            try:
                self.mcp_client = MCPClient(server_cmd)
                # MCPClient.connect() returns an async context manager that yields the client
                self._connection = self.mcp_client.connect()
                self.mcp_client = await asyncio.wait_for(
                    self._connection.__aenter__(),
                    timeout=self.config.timeout
                )
                break
            except asyncio.TimeoutError:
                if attempt < self.config.max_retries - 1:
                    logger.warning(
                        f"Connection attempt {attempt + 1} timed out, retrying..."
                    )
                    await self._cleanup()
                    await asyncio.sleep(2)
                else:
                    raise RuntimeError(
                        f"Failed to connect to MCP server after {self.config.max_retries} attempts"
                    )
            except Exception as e:
                logger.error(f"Connection error: {e}")
                await self._cleanup()
                raise RuntimeError(f"Failed to start MCP server: {e}")
        
        # Discover available tools
        await self._discover_tools()
        
        # Connect to the model source
        await self._connect_to_source(source)
        self._loaded_source = source
    
    async def _discover_tools(self) -> None:
        """Discover available MCP tools via feature detection."""
        if self.mcp_client is None:
            return
        
        # Try to list tools via MCP protocol
        try:
            # Note: This is a placeholder - actual tool discovery would use
            # the MCP list_tools() method when available
            # For now, we assume standard Modeling MCP tools
            self._available_tools = {
                "connection_operations",
                "model_operations",
                "table_operations",
                "database_operations",
            }
            logger.info(f"Discovered {len(self._available_tools)} MCP tools")
        except Exception as e:
            logger.warning(f"Tool discovery failed: {e}")
            # Fallback to assumed tool set
            self._available_tools = {
                "connection_operations",
                "model_operations",
                "table_operations",
            }
    
    async def _connect_to_source(self, source: str) -> None:
        """Connect to a Power BI model source.
        
        Args:
            source: PBIP folder path or connection string
            
        Raises:
            FileNotFoundError: If PBIP folder doesn't exist
            RuntimeError: If connection fails
        """
        if self.mcp_client is None:
            raise RuntimeError("MCP client not initialized")
        
        # Detect source type
        source_path = Path(source)
        
        if source_path.exists() and source_path.is_dir():
            # PBIP folder - connect via ConnectFolder
            await self._connect_pbip_folder(str(source_path))
        elif source.startswith("powerbi://") or source.startswith("localhost:"):
            # Connection string - connect via Connect
            await self._connect_via_connection_string(source)
        else:
            raise ValueError(
                f"Unsupported source type: {source}. "
                "Expected PBIP folder or connection string (powerbi://...)"
            )
    
    async def _connect_pbip_folder(self, folder_path: str) -> None:
        """Connect to a PBIP folder.
        
        Args:
            folder_path: Path to PBIP folder
            
        Raises:
            RuntimeError: If connection fails
        """
        logger.info(f"Connecting to PBIP folder: {folder_path}")
        
        try:
            result = await self.mcp_client.call_tool(
                "connection_operations",
                {
                    "request": {
                        "operation": "ConnectFolder",
                        "folderPath": folder_path,
                    }
                }
            )
            
            # Parse the result
            parsed = _parse_mcp_result(result)
            
            # Extract connection ID from result
            if parsed.get("success") and "data" in parsed:
                self._connection_id = parsed["data"].get("connectionName")
                logger.info(f"Connected with connection ID: {self._connection_id}")
            else:
                logger.warning("No connection ID returned, using default")
        
        except Exception as e:
            raise RuntimeError(f"Failed to connect to PBIP folder: {e}")
    
    async def _connect_via_connection_string(self, connection_string: str) -> None:
        """Connect via connection string.
        
        Args:
            connection_string: Connection string (powerbi://... or localhost:port)
            
        Raises:
            RuntimeError: If connection fails
        """
        logger.info(f"Connecting to: {connection_string}")
        
        try:
            # Parse connection string
            if connection_string.startswith("powerbi://"):
                # Fabric workspace connection
                result = await self.mcp_client.call_tool(
                    "connection_operations",
                    {
                        "request": {
                            "operation": "ConnectFabric",
                            "dataSource": connection_string,
                        }
                    }
                )
            else:
                # Desktop or XMLA endpoint
                result = await self.mcp_client.call_tool(
                    "connection_operations",
                    {
                        "request": {
                            "operation": "Connect",
                            "connectionString": connection_string,
                        }
                    }
                )
            
            if isinstance(result, dict) and "connectionName" in result:
                self._connection_id = result["connectionName"]
                logger.info(f"Connected with connection ID: {self._connection_id}")
        
        except Exception as e:
            raise RuntimeError(f"Failed to connect: {e}")
    
    async def extract_metadata(self) -> ModelMetadata:
        """Extract all metadata from the loaded model.
        
        Returns:
            ModelMetadata: Container with all extracted metadata
            
        Raises:
            RuntimeError: If no model is loaded
        """
        if self.mcp_client is None:
            raise RuntimeError("No model loaded. Call load_model() first.")
        
        logger.info("Extracting metadata from model...")
        
        # Extract model summary
        summary = await self._get_model_info()
        
        # Extract tables
        tables = await self._get_tables()
        
        # Extract measures
        measures = await self._get_measures()
        
        # Extract relationships
        relationships = await self._get_relationships()
        
        logger.info(
            f"Extracted {len(tables)} tables, {len(measures)} measures, "
            f"{len(relationships)} relationships"
        )
        
        return ModelMetadata(
            summary=summary,
            tables=tables,
            measures=measures,
            relationships=relationships,
            power_query=None,  # Not supported via Modeling MCP yet
        )
    
    async def _get_model_info(self) -> dict[str, Any]:
        """Get model summary information.
        
        Returns:
            Dictionary with model summary
        """
        try:
            result = await self.mcp_client.call_tool(
                "model_operations",
                {
                    "request": {
                        "operation": "Get",
                        "connectionName": self._connection_id,
                    }
                }
            )
            
            parsed = _parse_mcp_result(result)
            
            if parsed.get("success") and "data" in parsed:
                data = parsed["data"]
                return {
                    "name": data.get("name", "Unknown"),
                    "description": data.get("description", ""),
                    "culture": data.get("culture", ""),
                }
            
            return {"name": "Unknown"}
        
        except Exception as e:
            logger.warning(f"Failed to get model info: {e}")
            return {"name": "Unknown"}
    
    async def _get_tables(self) -> list[Table]:
        """Get all tables from the model.
        
        Returns:
            List of Table objects
        """
        try:
            result = await self.mcp_client.call_tool(
                "table_operations",
                {
                    "request": {
                        "operation": "List",
                        "connectionName": self._connection_id,
                    }
                }
            )
            
            parsed = _parse_mcp_result(result)
            
            tables = []
            if parsed.get("success") and "data" in parsed:
                for table_data in parsed["data"]:
                    if isinstance(table_data, dict):
                        # Get table schema
                        schema = await self._get_table_schema(table_data.get("name", ""))
                        
                        tables.append(Table(
                            name=table_data.get("name", ""),
                            columns=schema,
                            row_count=None,  # Not available via Modeling MCP
                        ))
            
            return tables
        
        except Exception as e:
            logger.error(f"Failed to get tables: {e}")
            return []
    
    async def _get_table_schema(self, table_name: str) -> list[dict]:
        """Get schema for a specific table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column definitions
        """
        try:
            result = await self.mcp_client.call_tool(
                "table_operations",
                {
                    "request": {
                        "operation": "GetSchema",
                        "connectionName": self._connection_id,
                        "tableName": table_name,
                    }
                }
            )
            
            parsed = _parse_mcp_result(result)
            if parsed.get("success") and "data" in parsed:
                table_data = parsed["data"]
                # GetSchema returns {"TableName":"X", "Columns":[], "Measures":[], "Relationships":[]}
                if isinstance(table_data, dict) and "Columns" in table_data:
                    columns = []
                    for col in table_data["Columns"]:
                        if isinstance(col, dict):
                            columns.append({
                                "ColumnName": col.get("name", col.get("ColumnName", "")),
                                "DataType": col.get("dataType", col.get("DataType", "string")),
                                "IsHidden": col.get("isHidden", col.get("IsHidden", False)),
                            })
                    return columns
            
            return []
        
        except Exception as e:
            logger.warning(f"Failed to get schema for table {table_name}: {e}")
            return []
    
    async def _get_measures(self) -> list[Measure]:
        """Get all measures from the model.
        
        Returns:
            List of Measure objects
        """
        try:
            # Note: Measures are typically part of tables in Modeling MCP
            # We need to query each table for its measures
            result = await self.mcp_client.call_tool(
                "table_operations",
                {
                    "request": {
                        "operation": "List",
                        "connectionName": self._connection_id,
                    }
                }
            )
            
            measures = []
            parsed = _parse_mcp_result(result)
            if parsed.get("success") and "data" in parsed:
                for table_data in parsed["data"]:
                    if isinstance(table_data, dict):
                        table_name = table_data.get("name", "")
                        # Get measures for this table
                        table_measures = await self._get_table_measures(table_name)
                        measures.extend(table_measures)
            
            return measures
        
        except Exception as e:
            logger.error(f"Failed to get measures: {e}")
            return []
    
    async def _get_table_measures(self, table_name: str) -> list[Measure]:
        """Get measures for a specific table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of Measure objects
        """
        try:
            # Use GetSchema which returns table structure including measures
            result = await self.mcp_client.call_tool(
                "table_operations",
                {
                    "request": {
                        "operation": "GetSchema",
                        "connectionName": self._connection_id,
                        "tableName": table_name,
                    }
                }
            )
            
            measures = []
            parsed = _parse_mcp_result(result)
            if parsed.get("success") and "data" in parsed:
                table_data = parsed["data"]
                # GetSchema returns {"TableName":"X", "Columns":[], "Measures":[], "Relationships":[]}
                if isinstance(table_data, dict) and "Measures" in table_data:
                    for measure_data in table_data["Measures"]:
                        if isinstance(measure_data, dict):
                            measures.append(Measure(
                                name=measure_data.get("name", ""),
                                table=table_name,
                                expression=measure_data.get("expression", ""),
                                description=measure_data.get("description"),
                                format_string=measure_data.get("formatString"),
                                is_hidden=measure_data.get("isHidden", False),
                                display_folder=measure_data.get("displayFolder"),
                            ))
            
            return measures
        
        except Exception as e:
            logger.warning(f"Failed to get measures for table {table_name}: {e}")
            return []
    
    async def _get_relationships(self) -> list[Relationship]:
        """Get all relationships from the model.
        
        Returns:
            List of Relationship objects
        """
        try:
            # Try relationship_operations List to get all model relationships
            result = await self.mcp_client.call_tool(
                "relationship_operations",
                {
                    "request": {
                        "operation": "List",
                        "connectionName": self._connection_id,
                    }
                }
            )
            
            relationships = []
            parsed = _parse_mcp_result(result)
            if parsed.get("success") and "data" in parsed:
                rel_list = parsed["data"]
                for rel_data in rel_list:
                    if isinstance(rel_data, dict):
                        relationships.append(Relationship(
                            from_table=rel_data.get("fromTable", ""),
                            from_column=rel_data.get("fromColumn", ""),
                            to_table=rel_data.get("toTable", ""),
                            to_column=rel_data.get("toColumn", ""),
                            is_active=rel_data.get("isActive", True),
                            cross_filter_direction=rel_data.get("crossFilteringBehavior", rel_data.get("crossFilterDirection", "Single")),
                        ))
            
            return relationships
        
        except Exception as e:
            logger.error(f"Failed to get relationships: {e}")
            return []
    
    async def _cleanup(self) -> None:
        """Clean up MCP client resources."""
        if self._connection is not None:
            try:
                await self._connection.__aexit__(None, None, None)
            except Exception as e:
                logger.warning(f"Error during cleanup: {e}")
            finally:
                self._connection = None
                self.mcp_client = None  # type: ignore
    
    async def close(self) -> None:
        """Close the MCP connection and release resources."""
        if self._connection_id and self.mcp_client:
            try:
                # Disconnect from model
                await self.mcp_client.call_tool(
                    "connection_operations",
                    {
                        "request": {
                            "operation": "Disconnect",
                            "connectionName": self._connection_id,
                        }
                    }
                )
            except Exception as e:
                logger.warning(f"Error disconnecting: {e}")
        
        await self._cleanup()
        self._loaded_source = None
        self._connection_id = None
