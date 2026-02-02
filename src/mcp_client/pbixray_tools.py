# src/mcp_client/pbixray_tools.py
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any
from .client import MCPClient


@dataclass
class Table:
    name: str
    columns: list[dict]
    row_count: int | None = None


@dataclass
class Measure:
    name: str
    table: str
    expression: str
    description: str | None = None
    format_string: str | None = None
    is_hidden: bool = False
    display_folder: str | None = None


@dataclass
class Relationship:
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    is_active: bool
    cross_filter_direction: str


class PBIXRayClient:
    """High-level client for PBIXRay MCP server."""
    
    def __init__(self, client: MCPClient):
        self.client = client
    
    async def load_pbix(self, file_path: str) -> dict:
        """Load a PBIX file for analysis."""
        if not Path(file_path).exists():
            raise FileNotFoundError(f"PBIX file not found: {file_path}")
        
        result = await self.client.call_tool("load_pbix", {"file_path": file_path})
        return self._parse_result(result)
    
    async def get_tables(self) -> list[Table]:
        """Get all tables from the loaded model."""
        result = await self.client.call_tool("get_tables", {})
        data = self._parse_result(result)
        
        tables = []
        for table_data in data:
            tables.append(Table(
                name=table_data.get("name", ""),
                columns=table_data.get("columns", []),
                row_count=table_data.get("row_count")
            ))
        return tables
    
    async def get_measures(self) -> list[Measure]:
        """Get all measures from the loaded model."""
        result = await self.client.call_tool("get_measures", {})
        data = self._parse_result(result)
        
        measures = []
        for measure_data in data:
            measures.append(Measure(
                name=measure_data.get("name", ""),
                table=measure_data.get("table", ""),
                expression=measure_data.get("expression", ""),
                description=measure_data.get("description"),
                format_string=measure_data.get("format_string"),
                is_hidden=measure_data.get("is_hidden", False),
                display_folder=measure_data.get("display_folder")
            ))
        return measures
    
    async def get_relationships(self) -> list[Relationship]:
        """Get all relationships from the loaded model."""
        result = await self.client.call_tool("get_relationships", {})
        data = self._parse_result(result)
        
        relationships = []
        for rel_data in data:
            relationships.append(Relationship(
                from_table=rel_data.get("from_table", ""),
                from_column=rel_data.get("from_column", ""),
                to_table=rel_data.get("to_table", ""),
                to_column=rel_data.get("to_column", ""),
                is_active=rel_data.get("is_active", True),
                cross_filter_direction=rel_data.get("cross_filter_direction", "OneWay")
            ))
        return relationships
    
    async def get_schema(self, table_name: str) -> dict:
        """Get detailed schema for a specific table."""
        result = await self.client.call_tool("get_schema", {"table_name": table_name})
        return self._parse_result(result)
    
    async def get_power_query(self) -> str:
        """Get Power Query/M code from the model."""
        result = await self.client.call_tool("get_power_query", {})
        data = self._parse_result(result)
        return data if isinstance(data, str) else json.dumps(data, indent=2)
    
    async def get_model_summary(self) -> dict:
        """Get summary statistics about the model."""
        result = await self.client.call_tool("get_model_summary", {})
        return self._parse_result(result)
    
    def _parse_result(self, result: dict) -> Any:
        """Parse MCP tool result and extract content."""
        if not result:
            return {}
        
        # MCP returns results in content array
        content = result.get("content", [])
        if not content:
            return {}
        
        # Extract text content
        text_content = content[0].get("text", "")
        
        # Try to parse as JSON
        try:
            return json.loads(text_content)
        except (json.JSONDecodeError, TypeError):
            return text_content
