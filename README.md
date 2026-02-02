# Power BI Auto-Documentation Pipeline

Automatically generate comprehensive GitHub wiki documentation from Power BI PBIX files using the Model Context Protocol (MCP).

## Overview

This project implements a three-layer pipeline that extracts metadata from Power BI models and transforms it into structured, searchable wiki documentation with Mermaid diagrams.

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

# Install project dependencies
pip install -r requirements.txt
```

**Note for Windows Users**: The `xpress9` dependency (used by `pbixray`) requires Cython and may fail to build on Windows. 

**Workaround options:**
1. Use **WSL (Windows Subsystem for Linux)** where the build succeeds
2. Use **Microsoft's Remote MCP Server** (hosted at `api.fabric.microsoft.com/v1/mcp/powerbi`) with Entra ID authentication
3. Use **Microsoft's Modeling MCP Server** to connect to Power BI Desktop instances or PBIP folders

## Usage

### Local Generation

Generate documentation locally from a PBIX file:

```bash
python generate_wiki.py ./path/to/your/model.pbix -o ./wiki-preview
```

Example from the articles:
```bash
python generate_wiki.py ./models/Sales.pbix -o ./wiki -n "Sales Analytics Model"
```

### Running Locally (from the articles)

Test the pipeline before deploying. After completing the installation steps, run:

```bash
# Clone your generator repo
git clone https://github.com/your-org/pbi-wiki-generator
cd pbi-wiki-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (including pbixray-mcp-server setup from earlier)
pip install -r requirements.txt

# Generate wiki locally
python generate_wiki.py ./path/to/your/model.pbix -o ./wiki-preview

# Preview the output
ls -la ./wiki-preview/
cat ./wiki-preview/Home.md
```

### GitHub Actions Integration

The pipeline automatically generates documentation when you push PBIX files:

1. Enable wiki for your repository (Settings → Features → Wikis)

2. The workflow triggers on:
   - Push of any `.pbix` file
   - Manual dispatch via Actions tab

3. Documentation is automatically committed to the wiki repository

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

You can use different MCP servers:

**PBIXRay** (default):
- Works directly with PBIX files
- Ideal for CI/CD pipelines

**Microsoft Modeling MCP Server**:
- Connects to Power BI Desktop or PBIP folders
- Comprehensive metadata access

**Microsoft Remote MCP Server**:
- Hosted at `api.fabric.microsoft.com/v1/mcp/powerbi`
- Entra ID authentication
- Access to published semantic models

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

- [PBIXRay MCP Server](https://github.com/jonaolden/pbixray-mcp-server) by jonaolden
- [PBIXRay Library](https://github.com/Hugoberry/pbixray) by Hugoberry
- [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic
- Article series by [Michael Hannecke](https://medium.com/@michael.hannecke)
