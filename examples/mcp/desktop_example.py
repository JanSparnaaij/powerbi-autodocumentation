"""Example: Document a Power BI Desktop instance using MCP engine."""

import asyncio
import logging

from src.engines import get_engine
from src.engines.mcp import MCPEngineConfig, MCPMode


async def main():
    """Generate documentation from Power BI Desktop live connection."""
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Configuration
    desktop_connection = "localhost:12345"  # Power BI Desktop XMLA endpoint
    output_dir = "./docs"
    
    # Create MCP engine config
    config = MCPEngineConfig(
        server_path=None,  # Auto-discover
        mode=MCPMode.READONLY,
        timeout=120,  # Longer timeout for Desktop connections
        max_retries=3
    )
    
    print("=" * 60)
    print("Power BI Desktop Live Documentation")
    print("=" * 60)
    print()
    print("Prerequisites:")
    print("1. Power BI Desktop must be running")
    print("2. XMLA endpoint must be enabled:")
    print("   - File → Options → Preview features")
    print("   - Enable 'Power BI Desktop XMLA endpoint'")
    print("   - Restart Desktop")
    print()
    print(f"Connecting to: {desktop_connection}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Create engine
    engine = get_engine("mcp", config=config)
    
    # Extract metadata
    try:
        async with engine:
            # Load from Desktop
            print("Connecting to Power BI Desktop...")
            await engine.load_model(f"powerbi://{desktop_connection}")
            
            # Extract all metadata
            print("Extracting metadata...")
            metadata = await engine.extract_metadata()
            
            # Display results
            print("\nExtraction complete!")
            print(f"  Model: {metadata.summary.get('name', 'Unknown')}")
            print(f"  Tables: {len(metadata.tables)}")
            print(f"  Measures: {len(metadata.measures)}")
            print(f"  Relationships: {len(metadata.relationships)}")
            
            # List tables with column counts
            print("\nTables:")
            for table in metadata.tables:
                hidden = " (hidden)" if any(
                    col.get("IsHidden", False) for col in table.columns
                ) else ""
                print(f"  - {table.name}{hidden}")
                print(f"    Columns: {len(table.columns)}")
            
            # List measures by table
            if metadata.measures:
                print("\nMeasures by Table:")
                measures_by_table = {}
                for measure in metadata.measures:
                    if measure.table not in measures_by_table:
                        measures_by_table[measure.table] = []
                    measures_by_table[measure.table].append(measure)
                
                for table, measures in sorted(measures_by_table.items()):
                    print(f"  {table}:")
                    for measure in measures[:3]:  # Show first 3
                        print(f"    - {measure.name}")
                    if len(measures) > 3:
                        print(f"    ... and {len(measures) - 3} more")
            
            # Show relationships
            if metadata.relationships:
                print(f"\nRelationships:")
                for rel in metadata.relationships[:5]:  # Show first 5
                    direction = "⟷" if rel.cross_filter_direction == "Both" else "→"
                    active = "●" if rel.is_active else "○"
                    print(
                        f"  {active} {rel.from_table}[{rel.from_column}] "
                        f"{direction} {rel.to_table}[{rel.to_column}]"
                    )
                if len(metadata.relationships) > 5:
                    print(f"  ... and {len(metadata.relationships) - 5} more")
            
            print("\n✓ Successfully documented Desktop model")
            print(f"\nNext steps:")
            print(f"  1. Review extracted metadata")
            print(f"  2. Generate wiki pages with WikiGenerator")
            print(f"  3. Commit to repository")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  - Verify Power BI Desktop is running")
        print("  - Check XMLA endpoint is enabled")
        print("  - Try different port number (check Desktop options)")
        print("  - Increase timeout with --mcp-timeout")
        raise


if __name__ == "__main__":
    asyncio.run(main())
