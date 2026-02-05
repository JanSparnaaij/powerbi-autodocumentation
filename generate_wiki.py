# generate_wiki.py
import argparse
import asyncio
import logging
from src.generators.wiki_generator import WikiGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Generate documentation from Power BI models (PBIX, PBIP, or live connections)"
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="Path to PBIX file, PBIP folder, or connection string"
    )
    parser.add_argument(
        "-o", "--output",
        default="./docs",
        help="Output directory for documentation pages (default: ./docs)"
    )
    parser.add_argument(
        "-n", "--name",
        help="Model name (default: derived from source)"
    )
    
    # Engine selection
    parser.add_argument(
        "--engine",
        choices=["pbixray", "mcp"],
        default="pbixray",
        help="Documentation engine to use (default: pbixray). "
             "Use 'mcp' for PBIP folders or Power BI Desktop connections."
    )
    
    # MCP engine options
    mcp_group = parser.add_argument_group("MCP Engine Options")
    mcp_group.add_argument(
        "--mcp-server",
        help="Path to PowerBI.ModelingMcp.Server.exe (auto-discovered if not specified)"
    )
    mcp_group.add_argument(
        "--mcp-mode",
        choices=["readonly", "readwrite"],
        default="readonly",
        help="MCP server access mode (default: readonly)"
    )
    mcp_group.add_argument(
        "--mcp-timeout",
        type=int,
        default=60,
        help="MCP connection timeout in seconds (default: 60)"
    )
    mcp_group.add_argument(
        "--mcp-retries",
        type=int,
        default=3,
        help="Maximum MCP connection retry attempts (default: 3)"
    )
    
    # Convenience flags
    parser.add_argument(
        "--pbip",
        metavar="FOLDER",
        help="Shortcut for --engine mcp with PBIP folder path"
    )
    parser.add_argument(
        "--desktop",
        metavar="CONNECTION",
        help="Shortcut for --engine mcp with Desktop connection string"
    )
    
    # Logging
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Handle convenience flags
    if args.pbip:
        args.engine = "mcp"
        args.source = args.pbip
    elif args.desktop:
        args.engine = "mcp"
        args.source = args.desktop
    elif not args.source:
        parser.error("source is required (or use --pbip/--desktop)")
    
    # Build engine kwargs
    engine_kwargs = {}
    if args.engine == "mcp":
        engine_kwargs = {
            "server_path": args.mcp_server,
            "mode": args.mcp_mode,
            "timeout": args.mcp_timeout,
            "max_retries": args.mcp_retries,
        }
    
    generator = WikiGenerator(args.output)
    asyncio.run(generator.generate(
        args.source,
        model_name=args.name,
        engine_type=args.engine,
        engine_kwargs=engine_kwargs
    ))


if __name__ == "__main__":
    main()
