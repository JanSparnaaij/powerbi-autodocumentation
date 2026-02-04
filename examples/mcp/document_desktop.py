"""Example: Connect to Power BI Desktop and extract metadata.

This example shows how to connect to a running Power BI Desktop instance
and extract model metadata using the MCP Modeling engine.

Prerequisites:
1. Power BI Desktop must be running
2. XMLA endpoint must be enabled (File → Options → Preview features)
3. Note the port number from: File → Options → Security → "Data connectivity" 
   Or check: localhost:XXXXX (shown in Desktop during connection)
"""

import asyncio
import logging
from src.engines.mcp import ModelingMCPEngine, MCPEngineConfig, MCPMode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def document_desktop_instance(port: int | None = None):
    """Document a Power BI Desktop instance.
    
    Args:
        port: Desktop XMLA endpoint port (if known). If None, will prompt.
    """
    
    if port is None:
        # Prompt for port
        print("\n=== Power BI Desktop Connection ===")
        print("1. Open Power BI Desktop")
        print("2. Enable XMLA endpoint: File → Options → Preview features")
        print("3. Restart Desktop if needed")
        print("4. The port is usually shown in connection dialogs")
        print("   Common ports: 51174, 51175, 51176, etc.")
        port_str = input("\nEnter Desktop port number: ")
        try:
            port = int(port_str)
        except ValueError:
            logger.error("Invalid port number")
            return
    
    # Build connection string
    connection_string = f"localhost:{port}"
    
    # Configure the MCP engine
    config = MCPEngineConfig(
        server_path=None,  # Auto-discover
        mode=MCPMode.READONLY,
        timeout=120,  # Longer timeout for Desktop
        skip_confirmation=True,
    )
    
    # Create engine
    engine = ModelingMCPEngine(config)
    
    try:
        # Connect to Desktop
        logger.info(f"Connecting to Desktop at: {connection_string}")
        await engine.load_model(connection_string)
        
        # Extract metadata
        logger.info("Extracting metadata...")
        metadata = await engine.extract_metadata()
        
        # Display results
        print("\n" + "="*60)
        print(f"Model: {metadata.summary.get('name', 'Unknown')}")
        print(f"Description: {metadata.summary.get('description', 'N/A')}")
        print(f"Culture: {metadata.summary.get('culture', 'N/A')}")
        print("="*60)
        
        print(f"\n📊 Tables: {len(metadata.tables)}")
        for table in metadata.tables:
            print(f"   • {table.name} ({len(table.columns)} columns)")
        
        print(f"\n📏 Measures: {len(metadata.measures)}")
        for measure in metadata.measures[:10]:  # First 10
            print(f"   • {measure.table}.{measure.name}")
            if measure.description:
                print(f"     ↳ {measure.description}")
        
        if len(metadata.measures) > 10:
            print(f"   ... and {len(metadata.measures) - 10} more")
        
        print(f"\n🔗 Relationships: {len(metadata.relationships)}")
        for rel in metadata.relationships:
            direction = "⟷" if rel.cross_filter_direction == "Both" else "→"
            active = "✓" if rel.is_active else "✗"
            print(f"   {active} {rel.from_table}[{rel.from_column}] {direction} {rel.to_table}[{rel.to_column}]")
        
        print("\n✓ Successfully extracted metadata from Desktop")
        print(f"\nTo generate full documentation, run:")
        print(f"  python generate_wiki.py --desktop {connection_string} -o ./docs")
    
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Verify Power BI Desktop is running")
        print("2. Check XMLA endpoint is enabled")
        print("3. Verify the port number is correct")
        print("4. Try a different port (Desktop uses dynamic ports)")
        raise
    
    finally:
        await engine.close()


if __name__ == "__main__":
    # Example: Connect to Desktop on port 51174
    # Change this to your Desktop's port number
    asyncio.run(document_desktop_instance(port=None))  # Will prompt
    
    # Or specify port directly:
    # asyncio.run(document_desktop_instance(port=51174))
