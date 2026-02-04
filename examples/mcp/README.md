# MCP Engine Examples

This folder contains examples for using the Power BI Modeling MCP engine.

## Prerequisites

1. **Install Power BI VS Code Extension**:
   - Open VS Code
   - Install "Power BI" extension by Microsoft
   - Or download from: https://marketplace.visualstudio.com/items?itemName=microsoft.powerbi-vscode

2. **Verify Installation**:
   ```bash
   # Windows
   dir "%USERPROFILE%\.vscode\extensions\microsoft.powerbi-vscode*"
   
   # The PowerBI.ModelingMcp.Server.exe should be in the extension folder
   ```

3. **Set Environment Variable** (optional):
   ```bash
   # Windows
   set POWERBI_MCP_PATH=C:\path\to\PowerBI.ModelingMcp.Server.exe
   
   # Linux/Mac
   export POWERBI_MCP_PATH=/path/to/PowerBI.ModelingMcp.Server
   ```

## Example 1: PBIP Folder

Document a PBIP folder (TMDL format):

```bash
# Using convenience flag
python generate_wiki.py --pbip ./Sales.Dataset -o ./docs

# Or with explicit engine
python generate_wiki.py ./Sales.Dataset --engine mcp -o ./docs
```

## Example 2: Power BI Desktop Live Connection

Document a currently running Power BI Desktop instance:

### Step 1: Enable XMLA endpoint in Desktop

1. Open Power BI Desktop
2. File → Options and settings → Options
3. Preview features → Enable "Power BI Desktop XMLA endpoint"
4. Restart Desktop

### Step 2: Get the port number

1. Open your PBIX file
2. File → Options and settings → Options
3. Preview features → "Store datasets using enhanced metadata format" (should be checked)
4. The port is typically 12345 or auto-assigned

### Step 3: Generate documentation

```bash
# Using convenience flag
python generate_wiki.py --desktop localhost:12345 -o ./docs

# Or with explicit connection
python generate_wiki.py powerbi://localhost:12345 --engine mcp -o ./docs
```

## Example 3: Custom Configuration

```bash
python generate_wiki.py ./Sales.Dataset -o ./docs \
  --engine mcp \
  --mcp-mode readonly \
  --mcp-timeout 120 \
  --mcp-retries 5 \
  --mcp-server "C:\custom\PowerBI.ModelingMcp.Server.exe" \
  --verbose
```

## Example 4: Python Script

```python
import asyncio
from src.engines import get_engine
from src.engines.mcp import MCPEngineConfig, MCPMode

async def main():
    # Create MCP engine with custom config
    config = MCPEngineConfig(
        server_path=None,  # Auto-discover
        mode=MCPMode.READONLY,
        timeout=120,
        max_retries=5
    )
    
    engine = get_engine("mcp", config=config)
    
    # Load and extract metadata
    async with engine:
        await engine.load_model("./Sales.Dataset")
        metadata = await engine.extract_metadata()
        
        print(f"Tables: {len(metadata.tables)}")
        print(f"Measures: {len(metadata.measures)}")
        print(f"Relationships: {len(metadata.relationships)}")

asyncio.run(main())
```

## Example 5: Analysis Services Connection

Connect to SQL Server Analysis Services:

```bash
python generate_wiki.py "Data Source=server.domain.com;Initial Catalog=AdventureWorks" \
  --engine mcp \
  --mcp-mode readonly \
  -o ./docs
```

## Troubleshooting

### Server Not Found

```
RuntimeError: Power BI Modeling MCP Server not found
```

**Solutions**:
1. Install Power BI VS Code extension
2. Set `POWERBI_MCP_PATH` environment variable
3. Provide explicit path via `--mcp-server` flag

### Connection Timeout

```
RuntimeError: Failed to connect to MCP server after 3 attempts
```

**Solutions**:
1. Increase timeout: `--mcp-timeout 120`
2. Increase retries: `--mcp-retries 5`
3. Check if server is accessible
4. Verify Desktop is running (for Desktop connections)

### Permission Denied

```
RuntimeError: Failed to connect: Access denied
```

**Solutions**:
1. Use `--mcp-mode readonly` (default)
2. For write operations, use `--mcp-mode readwrite` explicitly
3. Check Windows Firewall/antivirus settings

## Additional Resources

- [Power BI VS Code Extension Docs](https://learn.microsoft.com/en-us/power-bi/developer/vscode/overview)
- [XMLA Endpoint Documentation](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools)
- [TMDL Format Specification](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview)
