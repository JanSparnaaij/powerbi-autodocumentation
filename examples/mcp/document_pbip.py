"""Example: Using MCP engine programmatically to document a PBIP folder.

This example demonstrates how to use the MCP Modeling engine directly
from Python code to document a PBIP folder.
"""

import asyncio
import logging
from pathlib import Path
from src.engines.mcp import ModelingMCPEngine, MCPEngineConfig, MCPMode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def document_pbip_folder():
    """Document a PBIP folder using the MCP engine."""
    
    # Path to your PBIP folder
    pbip_folder = Path("./Sales.Dataset")
    
    if not pbip_folder.exists():
        logger.error(f"PBIP folder not found: {pbip_folder}")
        return
    
    # Configure the MCP engine
    config = MCPEngineConfig(
        server_path=None,  # Auto-discover from VS Code extension
        mode=MCPMode.READONLY,
        timeout=60,
        skip_confirmation=True,
    )
    
    # Create engine instance
    engine = ModelingMCPEngine(config)
    
    try:
        # Load the PBIP model
        logger.info(f"Loading PBIP folder: {pbip_folder}")
        await engine.load_model(str(pbip_folder))
        
        # Extract metadata
        logger.info("Extracting metadata...")
        metadata = await engine.extract_metadata()
        
        # Display summary
        logger.info(f"Model: {metadata.summary.get('name', 'Unknown')}")
        logger.info(f"Tables: {len(metadata.tables)}")
        logger.info(f"Measures: {len(metadata.measures)}")
        logger.info(f"Relationships: {len(metadata.relationships)}")
        
        # Print table details
        print("\nTables:")
        for table in metadata.tables:
            print(f"  - {table.name} ({len(table.columns)} columns)")
        
        # Print measure details
        print("\nMeasures:")
        for measure in metadata.measures[:5]:  # First 5 only
            print(f"  - {measure.name} (Table: {measure.table})")
        
        if len(metadata.measures) > 5:
            print(f"  ... and {len(metadata.measures) - 5} more")
        
        # Print relationship details
        print("\nRelationships:")
        for rel in metadata.relationships[:5]:  # First 5 only
            direction = "⟷" if rel.cross_filter_direction == "Both" else "→"
            active = "✓" if rel.is_active else "✗"
            print(f"  {active} {rel.from_table}.{rel.from_column} {direction} {rel.to_table}.{rel.to_column}")
        
        if len(metadata.relationships) > 5:
            print(f"  ... and {len(metadata.relationships) - 5} more")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
    
    finally:
        # Always close the engine
        await engine.close()


if __name__ == "__main__":
    asyncio.run(document_pbip_folder())
