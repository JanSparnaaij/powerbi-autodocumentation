"""Example: Document a PBIP folder using MCP engine."""

import asyncio
import logging
from pathlib import Path

from src.engines import get_engine
from src.engines.mcp import MCPEngineConfig, MCPMode


async def main():
    """Generate documentation from a PBIP folder."""
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Configuration
    pbip_folder = "./Sales.Dataset"  # Path to your PBIP folder
    output_dir = "./docs"
    
    # Create MCP engine config
    config = MCPEngineConfig(
        server_path=None,  # Auto-discover from VS Code extension
        mode=MCPMode.READONLY,  # Read-only access
        timeout=60,  # Connection timeout in seconds
        max_retries=3,  # Number of retry attempts
        skip_confirmation=True,  # Skip connection dialogs
        auto_start=True  # Automatically start the server
    )
    
    print(f"Generating documentation for PBIP: {pbip_folder}")
    print(f"Output directory: {output_dir}")
    
    # Create engine
    engine = get_engine("mcp", config=config)
    
    # Extract metadata
    async with engine:
        # Load the PBIP folder
        print("Loading PBIP folder...")
        await engine.load_model(pbip_folder)
        
        # Extract all metadata
        print("Extracting metadata...")
        metadata = await engine.extract_metadata()
        
        # Display results
        print("\nExtraction complete!")
        print(f"  Model: {metadata.summary.get('name', 'Unknown')}")
        print(f"  Tables: {len(metadata.tables)}")
        print(f"  Measures: {len(metadata.measures)}")
        print(f"  Relationships: {len(metadata.relationships)}")
        
        # List tables
        print("\nTables:")
        for table in metadata.tables:
            print(f"  - {table.name} ({len(table.columns)} columns)")
        
        # List measures
        if metadata.measures:
            print(f"\nMeasures (showing first 5):")
            for measure in metadata.measures[:5]:
                print(f"  - {measure.table}[{measure.name}]")
        
        # Now you could generate wiki pages using WikiGenerator
        # from src.generators.wiki_generator import WikiGenerator
        # generator = WikiGenerator(output_dir)
        # ... generate pages ...


if __name__ == "__main__":
    asyncio.run(main())
