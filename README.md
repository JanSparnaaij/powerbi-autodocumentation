# Power BI Auto-Documentation Pipeline

Automatically generate comprehensive GitHub wiki documentation from Power BI PBIX files using the Model Context Protocol (MCP).

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Installing Dependencies](#installing-dependencies)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Basic Usage (PBIXRay Engine)](#basic-usage-pbixray-engine)
  - [Using the MCP Modeling Engine](#using-the-mcp-modeling-engine)
  - [Engine Comparison](#engine-comparison)
  - [Local Generation](#local-generation)
  - [GitHub Actions Integration](#github-actions-integration)
- [Project Structure](#project-structure)
- [Generated Documentation](#generated-documentation)
- [Configuration](#configuration)
  - [Customizing Output](#customizing-output)
  - [Alternative MCP Servers](#alternative-mcp-servers)
  - [Creating Custom Engines](#creating-custom-engines)
- [Troubleshooting](#troubleshooting)
- [Series Articles](#series-articles)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

This project implements a three-layer pipeline that extracts metadata from Power BI models and transforms it into structured, searchable wiki documentation with Mermaid diagrams.

**📁 See [STRUCTURE.md](STRUCTURE.md) for detailed folder organization**

### Features

- 🚀 **Automated Documentation**: Generates wiki pages automatically from PBIX files
- 📊 **Mermaid Diagrams**: Visual entity-relationship diagrams for model structure
- 🔄 **CI/CD Integration**: GitHub Actions workflow for automatic updates
- 📝 **Comprehensive Coverage**: Documents tables, measures, relationships, and Power Query code
- 🔍 **Searchable**: Full-text search across all documentation
- 📜 **Version History**: Git-tracked documentation changes

## Architecture

The pipeline consists of three main components:

1. **MCP Client Layer** - Wraps the PBIXRay MCP server with typed Python functions
2. **Generator Layer** - Transforms metadata into Markdown pages with Mermaid diagrams
3. **Automation Layer** - GitHub Action that watches for PBIX changes and updates the wiki

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   PBIX File     │────▶│   MCP Server    │────▶│  Python Client  │
│  (or PBIP/TMDL) │     │   (PBIXRay)     │     │  (MCP Protocol) │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │  GitHub Wiki    │◀────│ Wiki Generator  │
                        │   (Markdown)    │     │ (Mermaid/MD)    │
                        └─────────────────┘     └─────────────────┘
```

## Installing Dependencies

The PBIXRay MCP server isn't available via pip. Clone it from GitHub:

```bash
# Clone the MCP server repository
git clone https://github.com/jonaolden/pbixray-mcp-server.git

# Make it accessible by adding to PYTHONPATH or installing in editable mode
pip install -e ./pbixray-mcp-server

# Install the base MCP protocol library and PBIXRay
pip install mcp pbixray
```

## Quick Start

```bash
# Activate virtual environment (if using one)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Generate documentation (outputs to docs/ by default)
python generate_wiki.py path/to/model.pbix

# Specify custom output folder
python generate_wiki.py path/to/model.pbix -o ./custom-output

# Use MCP engine for PBIP projects
python generate_wiki.py path/to/Model.SemanticModel --engine mcp

# Connect to Power BI Desktop (requires XMLA enabled)
python generate_wiki.py localhost:12345 --engine mcp
```

## Usage

### Basic Usage (PBIXRay Engine)

Generate documentation from a PBIX file using the default pbixray engine:

```bash
python generate_wiki.py ./path/to/your/model.pbix -o ./docs
```

Example with custom name:
```bash
python generate_wiki.py ./models/Sales.pbix -o ./docs -n "Sales Analytics Model"
```

### Using the MCP Modeling Engine

The MCP engine provides support for **PBIP folders**, **live Power BI Desktop connections**, and **Analysis Services** - features not available in pbixray.

#### Prerequisites

1. **Install Power BI Modeling MCP Server**:
   - Via VS Code: Install the "Power BI" extension by Microsoft
   - Or download from: https://github.com/microsoft/vscode-powerbi
   
2. **Set environment variable** (optional):
   ```bash
   # Windows
   set POWERBI_MCP_PATH=C:\path\to\PowerBI.ModelingMcp.Server.exe
   
   # Linux/Mac
   export POWERBI_MCP_PATH=/path/to/PowerBI.ModelingMcp.Server
   ```
   
   If not set, the tool will auto-discover from VS Code extension installation.

#### PBIP Folder Documentation

Generate documentation from a PBIP folder (TMDL format):

```bash
# Using convenience flag
python generate_wiki.py --pbip ./models/Sales.Dataset -o ./docs

# Or explicitly with engine selection
python generate_wiki.py ./models/Sales.Dataset -o ./docs --engine mcp
```

#### Power BI Desktop Live Connection

Document a currently open Power BI Desktop file:

```bash
# Auto-detect Desktop instance
python generate_wiki.py --desktop localhost:12345 -o ./docs

# Or with connection string
python generate_wiki.py powerbi://localhost:12345 -o ./docs --engine mcp
```

#### MCP Engine Options

```bash
python generate_wiki.py ./source -o ./docs --engine mcp \
  --mcp-mode readwrite \              # Access mode: readonly (default) or readwrite
  --mcp-timeout 120 \                 # Connection timeout in seconds (default: 60)
  --mcp-retries 5 \                   # Max retry attempts (default: 3)
  --mcp-server "C:\custom\path.exe"   # Custom server path
```

#### Complete MCP Example

```bash
# Document PBIP folder with custom timeout and verbose logging
python generate_wiki.py ./models/Sales.Dataset -o ./docs \
  --engine mcp \
  --mcp-mode readonly \
  --mcp-timeout 120 \
  --verbose
```

### Engine Comparison

| Feature | PBIXRay Engine | MCP Modeling Engine |
|---------|----------------|---------------------|
| PBIX files | ✅ Yes | ❌ No |
| PBIP folders | ❌ No | ✅ Yes |
| TMDL format | ❌ No | ✅ Yes |
| Desktop live | ❌ No | ✅ Yes |
| SSAS connections | ❌ No | ✅ Yes |
| Power Query | ✅ Yes | ⚠️ Limited |
| Auto-discovery | N/A | ✅ Yes |
| Read-write mode | N/A | ✅ Yes |

**Recommendation**: Use pbixray (default) for PBIX files in CI/CD pipelines. Use MCP engine for PBIP folders, development workflows with Desktop, or Analysis Services connections.

### GitHub Actions Integration

The pipeline automatically generates documentation when you push PBIX files:

1. **No wiki needed** - Documentation goes to `docs/` folder in your repository

2. The workflow triggers on:
   - Push of any `.pbix` file
   - Manual dispatch via Actions tab

3. Documentation is automatically committed to the repository

4. **Enable GitHub Pages** (optional):
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`, folder: `/docs`
   - Your docs will be at `https://yourusername.github.io/repo-name/`

### Manual Workflow Dispatch

Trigger documentation generation manually:

1. Go to Actions tab
2. Select "Generate Power BI Documentation"
3. Click "Run workflow"
4. Enter the path to your PBIX file
5. Click "Run workflow"

## Project Structure

```
powerbi-autodocumentation/
├── src/
│   ├── engines/                # Documentation engine abstraction
│   │   ├── __init__.py
│   │   ├── base.py            # IDocumentationEngine interface
│   │   ├── registry.py        # Engine factory and registry
│   │   ├── pbixray/           # PBIXRay engine (PBIX files)
│   │   │   ├── __init__.py
│   │   │   └── engine.py
│   │   └── mcp/               # MCP Modeling engine (PBIP/Desktop)
│   │       ├── __init__.py
│   │       ├── engine.py      # Main engine implementation
│   │       ├── config.py      # Configuration classes
│   │       └── discovery.py   # Server auto-discovery
│   ├── mcp_client/
│   │   ├── __init__.py
│   │   ├── client.py          # MCP protocol client
│   │   └── pbixray_tools.py   # PBIXRay tool wrappers
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── wiki_generator.py  # Main wiki builder
│   │   ├── mermaid.py         # Diagram generation
│   │   └── pages.py           # Individual page generators
│   └── utils/
│       ├── __init__.py
│       └── markdown.py        # Markdown formatting helpers
├── tests/
│   └── engines/               # Engine tests
│       ├── __init__.py
│       ├── test_registry.py
│       ├── test_mcp_config.py
│       └── test_mcp_discovery.py
├── .github/workflows/
│   └── generate-wiki.yml      # GitHub Action
├── generate_wiki.py           # CLI entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## Generated Documentation

The pipeline generates the following wiki pages:

- **Home**: Model overview with table of contents
- **Table-{Name}**: Detailed documentation for each table
  - Column definitions and data types
  - Source queries
  - Related measures
- **Measures**: All DAX measures with expressions and descriptions
- **Relationships**: Entity-relationship diagram and relationship details
- **Data-Sources**: Power Query/M code and data source configurations

## Configuration

### Customizing Output

Edit the page generators in `src/generators/pages.py` to customize:
- Page layouts
- Table formatting
- Additional metadata to include
- Custom sections

### Alternative MCP Servers

The tool supports pluggable documentation engines through an abstraction layer.

#### Built-in Engines

**PBIXRay Engine** (default - `--engine pbixray`):
- Works directly with PBIX files
- Ideal for CI/CD pipelines
- Full Power Query support
- No external dependencies
- Source: [pbixray-mcp-server](https://github.com/jonaolden/pbixray-mcp-server)

**MCP Modeling Engine** (`--engine mcp`):
- Connects to Power BI Desktop, PBIP folders, or Analysis Services
- Comprehensive metadata access via Microsoft's Modeling MCP Server
- Auto-discovers server from VS Code extension or `POWERBI_MCP_PATH`
- Supports read-only and read-write modes
- Source: [Power BI VS Code extension](https://marketplace.visualstudio.com/items?itemName=microsoft.powerbi-vscode)

#### Creating Custom Engines

Implement the `IDocumentationEngine` interface:

```python
from src.engines.base import IDocumentationEngine, ModelMetadata

class CustomEngine(IDocumentationEngine):
    async def load_model(self, source: str, **kwargs):
        # Load your model
        pass
    
    async def extract_metadata(self) -> ModelMetadata:
        # Extract and return metadata
        pass
    
    async def close(self):
        # Clean up resources
        pass

# Register your engine
from src.engines import register_engine
register_engine("custom", CustomEngine)
```

Then use it:
```bash
python generate_wiki.py ./model.xyz --engine custom -o ./docs
```

## Troubleshooting

### MCP Server Not Found

```
RuntimeError: Failed to connect to MCP server
```

**Solution**: Ensure pbixray-mcp-server is installed and in Python path:
```bash
pip install -e ./pbixray-mcp-server
```

### PBIX File Not Found

```
FileNotFoundError: PBIX file not found
```

**Solution**: Verify the file path is correct and the file exists

### GitHub Actions Permission Error

**Solution**: Ensure the workflow has `contents: write` permission in `generate-wiki.yml`

## Series Articles

This implementation is based on the following article series:

- [Part 1: Architecture & Concepts](https://medium.com/@michael.hannecke/automating-power-bi-documentation-with-mcp-architecture-concepts-part-1-7ede12a40bc2)
- [Part 2: Implementation](https://medium.com/@michael.hannecke/building-a-power-bi-auto-documentation-pipeline-implementation-part-2-3151241eb979)
- Part 3: AI Enhancement & Multi-Model (coming soon)
- Part 4: Enterprise Integration (coming soon)
- Part 5: Local LLMs with Ollama (coming soon)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - see LICENSE file for details

## Acknowledgments

- [Power BI Modeling MCP Server](https://github.com/microsoft/vscode-powerbi) by Microsoft - Official MCP server for PBIP, Desktop, and Analysis Services
- [PBIXRay MCP Server](https://github.com/jonaolden/pbixray-mcp-server) by jonaolden - Community MCP server for PBIX files
- [PBIXRay Library](https://github.com/Hugoberry/pbixray) by Hugoberry - Python library for extracting PBIX metadata
- [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic - Open protocol for AI-tool integration
- Article series by [Michael Hannecke](https://medium.com/@michael.hannecke)
