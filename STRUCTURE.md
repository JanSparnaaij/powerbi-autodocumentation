# Project Structure

```
powerbi-autodocumentation/
│
├── docs/                           # Generated documentation (committed to git)
│   ├── artificial-intelligence-sample/
│   ├── customer-profitability-sample/
│   ├── fabrikam-company-sales-report/
│   └── README.md                   # Index of all documented models
│
├── src/                            # Source code
│   ├── engines/                    # Documentation engine abstraction layer
│   │   ├── base.py                 # IDocumentationEngine interface
│   │   ├── registry.py             # Engine factory and registration
│   │   ├── pbixray/                # PBIXRay engine (PBIX files)
│   │   └── mcp/                    # MCP Modeling engine (PBIP/Desktop/SSAS)
│   │       ├── engine.py           # Main MCP engine implementation
│   │       ├── config.py           # Configuration dataclasses
│   │       └── discovery.py        # MCP server auto-discovery
│   ├── generators/                 # Documentation generators
│   │   └── wiki_generator.py      # Markdown + Mermaid generator
│   └── mcp_client/                 # MCP protocol client
│       └── client.py               # Async MCP client wrapper
│
├── tests/                          # Test suite
│   └── engines/                    # Engine tests
│       └── test_registry.py        # Engine registration tests
│
├── examples/                       # Example scripts
│   └── mcp/                        # MCP usage examples
│       └── document_desktop.py     # Desktop connection example
│
├── models/                         # Sample Power BI models (PBIP format)
│   └── Customer Profitability Sample.SemanticModel/
│
├── .github/workflows/              # GitHub Actions CI/CD
│   └── update-wiki.yml             # Auto-documentation workflow
│
├── generate_wiki.py                # Main CLI entrypoint
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── CHANGELOG.md                    # Version history
└── .gitignore                      # Git ignore rules

# Output Folders

- `docs/` - Generated documentation (committed to git for GitHub Pages)
- `test-docs/` - Temporary test outputs (gitignored)
- `wiki/`, `wiki-output/` - Legacy output folders (gitignored)

# Documentation Generation Flow

1. **Input**: PBIX file, PBIP folder, or live connection
2. **Engine**: pbixray (PBIX) or mcp (PBIP/Desktop/SSAS)
3. **Extraction**: Tables, measures, relationships, metadata
4. **Generation**: Markdown files with Mermaid diagrams
5. **Output**: `docs/{model-name}/` folder structure
   - Home.md - Model overview
   - Table-{name}.md - Table documentation
   - Measures.md - All measures
   - Relationships.md - ER diagram
   - Data-Sources.md - Data source info

# Default Behavior

```bash
# Generates documentation in ./docs/ by default
python generate_wiki.py model.pbix

# Output: ./docs/model/Home.md, Table-*.md, etc.
```
