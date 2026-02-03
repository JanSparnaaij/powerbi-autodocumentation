# src/generators/wiki_generator.py
import os
import asyncio
from pathlib import Path

from ..mcp_client.client import MCPClient
from ..mcp_client.pbixray_tools import PBIXRayClient
from .mermaid import generate_er_diagram
from .pages import (
    generate_home_page,
    generate_table_page,
    generate_measures_page,
    generate_relationships_page,
    generate_data_sources_page,
)


class WikiGenerator:
    """Generates GitHub wiki pages from PBIX model."""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def generate(self, pbix_path: str, model_name: str | None = None):
        """Generate complete wiki from PBIX file."""
        
        if not model_name:
            model_name = Path(pbix_path).stem
        
        print(f"Generating documentation for {model_name}...")
        
        # Start MCP server and extract metadata
        # pbixray-mcp-server uses src/pbixray_server.py
        server_script = "./pbixray-mcp-server/src/pbixray_server.py"
        
        if not Path(server_script).exists():
            raise RuntimeError(f"pbixray-mcp-server not found at {server_script}")
        
        server_cmd = ["python", server_script]
        print(f"Using pbixray-mcp-server at {server_script}")
        
        try:
            async with MCPClient(server_cmd).connect() as client:
                pbi = PBIXRayClient(client)
                
                print("Loading PBIX file...")
                await pbi.load_pbix(pbix_path)
                
                print("Extracting metadata...")
                summary = await pbi.get_model_summary()
                print(f"DEBUG: Summary data: {summary}")
                tables = await pbi.get_tables()
                measures = await pbi.get_measures()
                relationships = await pbi.get_relationships()
                
                print(f"Found {len(tables)} tables, {len(measures)} measures, {len(relationships)} relationships")
                
                # Get schema for each table and update table columns
                for table in tables:
                    schema = await pbi.get_schema(table.name)
                    # Debug first table schema
                    if table.name == tables[0].name:
                        print(f"DEBUG: First table '{table.name}' schema type: {type(schema)}")
                        if isinstance(schema, list) and len(schema) > 0:
                            print(f"DEBUG: First column structure: {schema[0]}")
                            print(f"DEBUG: First column keys: {list(schema[0].keys()) if isinstance(schema[0], dict) else 'not a dict'}")
                    
                    # Update table columns from schema
                    if isinstance(schema, list):
                        table.columns = schema
                    elif isinstance(schema, dict) and 'columns' in schema:
                        table.columns = schema['columns']
                
                # Get Power Query code
                power_query = await pbi.get_power_query()
        
        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise
        except RuntimeError as e:
            print(f"MCP Error: {e}")
            print("Ensure the pbixray-mcp-server is installed and accessible")
            raise
        
        # Generate pages
        print("Generating wiki pages...")
        self._write_page("Home", generate_home_page(
            model_name, summary, tables, measures
        ))
        
        for table in tables:
            page_name = f"Table-{self._slugify(table.name)}"
            self._write_page(page_name, generate_table_page(
                table, measures
            ))
        
        self._write_page("Measures", generate_measures_page(measures))
        
        er_diagram = generate_er_diagram(
            relationships,
            [t.name for t in tables]
        )
        self._write_page("Relationships", generate_relationships_page(
            relationships, er_diagram
        ))
        
        self._write_page("Data-Sources", generate_data_sources_page(power_query))
        
        print(f"✓ Documentation generated in {self.output_dir}")
        print(f"  - Home page")
        print(f"  - {len(tables)} table pages")
        print(f"  - Measures page")
        print(f"  - Relationships page")
        print(f"  - Data Sources page")
    
    def _write_page(self, page_name: str, content: str):
        """Write a wiki page to disk."""
        file_path = self.output_dir / f"{page_name}.md"
        file_path.write_text(content, encoding="utf-8")
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-safe slug."""
        return text.lower().replace(" ", "-").replace("_", "-")
