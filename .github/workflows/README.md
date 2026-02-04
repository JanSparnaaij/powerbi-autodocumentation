# GitHub Actions Workflow Documentation

## Overview

The `generate-wiki.yml` workflow automatically generates documentation for Power BI models using a **hybrid approach**:

- **PBIX files** → Linux runner with PBIXRay engine (fast)
- **PBIP folders** → Windows runner with Microsoft MCP engine (comprehensive)

## Architecture

```
Push/Manual Trigger
        │
        ├─────────────────────┬─────────────────────┐
        │                     │                     │
    Job 1: pbix-docs      Job 2: pbip-docs        │
    (ubuntu-latest)       (windows-latest)        │
        │                     │                     │
    PBIXRay Engine        MCP Engine              │
        │                     │                     │
    Process .pbix         Process .SemanticModel  │
        │                     │                     │
        └─────────────────────┴─────────────────────┤
                              │
                        Commit to docs/
```

## Triggers

### Automatic (Push)
Triggers when you push changes to:
- `**.pbix` - Any PBIX file
- `**.pbip` - Any PBIP project file
- `**.SemanticModel/**` - Any file in a SemanticModel folder
- `.github/workflows/generate-wiki.yml` - Workflow itself

### Manual (Workflow Dispatch)
Run manually from GitHub Actions tab with options:
- **file_path**: Path to PBIX file or PBIP folder
- **file_type**: Auto-detect, pbix, or pbip (optional)

## Jobs

### Job 1: `pbix-docs` (Linux)

**Purpose**: Fast documentation generation for PBIX files using PBIXRay.

**Runner**: `ubuntu-latest`

**Engine**: PBIXRay (direct library access, no MCP server needed)

**Steps**:
1. Checkout repository
2. Setup Python 3.11
3. Install dependencies + pbixray-mcp-server
4. Find changed PBIX files
5. Generate documentation (`python generate_wiki.py file.pbix`)
6. Commit to `docs/`

**Runs when**: PBIX files are detected

### Job 2: `pbip-docs` (Windows)

**Purpose**: Comprehensive documentation for PBIP folders using Microsoft MCP Server.

**Runner**: `windows-latest`

**Engine**: Microsoft Power BI Modeling MCP

**Steps**:
1. Checkout repository
2. Setup Python 3.11
3. Install dependencies
4. **Download & install Power BI MCP Server** (from VS Code marketplace)
5. Find changed PBIP folders (`.SemanticModel` or `.Dataset`)
6. Generate documentation (`python generate_wiki.py folder --engine mcp`)
7. Commit to `docs/`

**Runs when**: PBIP folders are detected

**Key difference**: Downloads official Microsoft MCP server (0.1.9) from marketplace as a VS Code extension package and extracts it.

## File Detection Logic

### Push Events

**PBIX Job**:
- Detects changed `*.pbix` files via `git diff`
- Falls back to all PBIX files if none changed

**PBIP Job**:
- Detects changed files within `.SemanticModel` or `.Dataset` folders
- Extracts unique folder paths from changed files
- Falls back to all PBIP folders if none changed

### Manual Dispatch

Both jobs respect the `file_type` input:
- `auto`: Auto-detect based on extension
- `pbix`: Force PBIX job only
- `pbip`: Force PBIP job only

## Commit Strategy

Both jobs commit independently to avoid conflicts:

1. Pull latest changes (`git pull --rebase`)
2. Add `docs/` folder
3. Commit with unique message:
   - PBIX: `"Auto-update PBIX documentation from <sha>"`
   - PBIP: `"Auto-update PBIP documentation from <sha>"`
4. Push to `main`

**Race condition handling**: 
- `git pull --rebase` before push
- Jobs run independently, may result in 2 commits
- Both succeed if they modify different files

## Outputs

All documentation is written to `docs/` folder with structure:
```
docs/
├── model-name-1/
│   ├── Home.md
│   ├── Measures.md
│   ├── Relationships.md
│   └── Table-*.md
└── model-name-2/
    └── ...
```

## Environment Variables

### PBIX Job (Linux)
- Python path from installed packages

### PBIP Job (Windows)
- `POWERBI_MCP_PATH`: Set automatically to downloaded MCP server executable
- Used by MCP engine for auto-discovery

## Limitations

### PBIX Job
- ✅ PBIX files only
- ✅ Fast (Linux runner)
- ❌ No PBIP support
- ❌ No Power Query M code extraction (limited)

### PBIP Job
- ✅ PBIP folders (TMDL format)
- ✅ Full metadata via MCP
- ❌ Windows runner (slower)
- ❌ No Fabric remote connections (authentication issues)
- ⚠️ Requires MCP server download (~18 MB)

## Troubleshooting

### PBIX Job Fails
- Check Python dependencies in `requirements.txt`
- Verify pbixray-mcp-server installation
- Check PBIX file is not corrupted

### PBIP Job Fails
- Check MCP server download succeeded
- Verify `.SemanticModel` or `.Dataset` folder structure
- Check `definition/` subfolder exists with `.tmdl` files
- Review verbose logs (`--verbose` flag is enabled)

### Both Jobs Run
Normal behavior when both PBIX and PBIP files change. Each job handles its own file type.

### No Commits
- Check if files actually changed
- Verify documentation wasn't already up-to-date
- Look for "No changes to commit" message

## Cost Considerations

### Linux Runner
- Free for public repos
- Fast execution (~2-3 minutes)

### Windows Runner
- 2x multiplier for billing on private repos
- Slower execution (~5-8 minutes including MCP download)
- Consider caching MCP server if running frequently

## Future Enhancements

Potential improvements:
- Cache MCP server installation between runs
- Parallel PBIP folder processing
- Support for Fabric workspace connections (needs auth solution)
- Consolidated commit strategy (single commit for both jobs)
