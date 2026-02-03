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
        
        result = await self.client.call_tool("load_pbix_file", {"file_path": file_path})
        return self._parse_result(result)
    
    async def get_tables(self) -> list[Table]:
        """Get all tables from the loaded model."""
        result = await self.client.call_tool("get_tables", {})
        data = self._parse_result(result)
        
        # Handle string response (Python-formatted list with <StringArray> header)
        if isinstance(data, str):
            print(f"DEBUG: Tables data is string, length={len(data)}")
            print(f"DEBUG: First 200 chars: {data[:200]}")
            
            # Remove <StringArray> header if present
            if data.strip().startswith('<StringArray>'):
                print("DEBUG: Removing <StringArray> header")
                data = data.strip()[len('<StringArray>'):].strip()
                print(f"DEBUG: After header removal, first 200 chars: {data[:200]}")
            
            try:
                import ast
                # Use ast.literal_eval for Python-formatted lists (single quotes, etc.)
                print("DEBUG: Attempting ast.literal_eval")
                data = ast.literal_eval(data)
                print(f"DEBUG: Successfully parsed to list with {len(data)} items")
            except (ValueError, SyntaxError) as e:
                print(f"Warning: Could not parse tables string: {e}")
                print(f"First 500 chars: {data[:500]}")
                return []
        
        # pbixray-mcp-server returns a simple list of table names
        if isinstance(data, list):
            tables = [Table(name=name, columns=[], row_count=None) for name in data if isinstance(name, str)]
            print(f"Successfully parsed {len(tables)} tables")
            return tables
        
        return []
    
    async def get_measures(self) -> list[Measure]:
        """Get all measures from the loaded model."""
        result = await self.client.call_tool("get_dax_measures", {})
        data = self._parse_result(result)
        
        # Debug: print first measure to see structure
        if isinstance(data, list) and len(data) > 0:
            print(f"DEBUG: First measure structure: {data[0]}")
        
        # Handle case where data might be a string or not a list
        if isinstance(data, str):
            print(f"Warning: get_measures returned string: {data[:200]}...")
            return []
        if not isinstance(data, list):
            print(f"Warning: get_measures returned non-list type: {type(data)}")
            return []
        
        measures = []
        for measure_data in data:
            if isinstance(measure_data, dict):
                measures.append(Measure(
                    name=measure_data.get("Name", ""),
                    table=measure_data.get("TableName", ""),
                    expression=measure_data.get("Expression", ""),
                    description=measure_data.get("Description"),
                    format_string=measure_data.get("FormatString"),
                    is_hidden=measure_data.get("IsHidden", False),
                display_folder=measure_data.get("DisplayFolder")
            ))
        return measures
    
    async def get_relationships(self) -> list[Relationship]:
        """Get all relationships from the loaded model."""
        result = await self.client.call_tool("get_relationships", {})
        data = self._parse_result(result)
        
        # Debug: print first relationship to see structure
        if isinstance(data, list) and len(data) > 0:
            print(f"DEBUG: First relationship structure: {data[0]}")
        
        # Handle case where data might be a string or not a list
        if isinstance(data, str):
            print(f"Warning: get_relationships returned string: {data[:200]}...")
            return []
        if not isinstance(data, list):
            print(f"Warning: get_relationships returned non-list type: {type(data)}")
            return []
        
        relationships = []
        for rel_data in data:
            if isinstance(rel_data, dict):
                relationships.append(Relationship(
                    from_table=rel_data.get("FromTableName") or rel_data.get("FromTable") or "",
                    from_column=rel_data.get("FromColumnName") or rel_data.get("FromColumn") or "",
                to_table=rel_data.get("ToTableName") or rel_data.get("ToTable") or "",
                to_column=rel_data.get("ToColumnName") or rel_data.get("ToColumn") or "",
                is_active=bool(rel_data.get("IsActive", rel_data.get("is_active", True))),
                cross_filter_direction=rel_data.get("CrossFilteringBehavior") or rel_data.get("CrossFilterDirection") or "OneWay"
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
        data = self._parse_result(result)
        
        # If string, wrap in dict; otherwise return as-is
        if isinstance(data, str):
            return {"summary_text": data}
        if isinstance(data, dict):
            return data
        return {}
    
    def _parse_result(self, result: Any) -> Any:
        """Parse MCP tool result and extract content."""
        if not result:
            return {}
        
        # MCP v1.0+ returns CallToolResult Pydantic object
        # Access content attribute directly, not as dict
        content = getattr(result, "content", [])
        if not content:
            return {}
        
        # Extract text content from first content item
        first_content = content[0]
        text_content = getattr(first_content, "text", "")
        
        # Try to parse as JSON
        try:
            return json.loads(text_content)
        except (json.JSONDecodeError, TypeError):
            return text_content
