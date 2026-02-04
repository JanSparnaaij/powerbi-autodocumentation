# GitHub Actions Workflow Documentation

## Overview

The `generate-wiki.yml` workflow automatically generates documentation for Power BI models.

**Current Status:**
- ✅ **PBIX files** → Linux runner with PBIXRay engine (fully working)
- ⚠️ **PBIP folders** → **DISABLED** due to Microsoft MCP server compatibility issues in GitHub Actions

> **Note:** The PBIP job is disabled until Microsoft resolves WinError 216 compatibility issues with the `powerbi-modeling-mcp.exe` in hosted runners. For PBIP documentation, use local execution or export as PBIX.

## Architecture

```
Push/Manual Trigger
        │
        ├─────────────────────┬─────────────────────┐
        │                     │                     │
    Job 1: pbix-docs      Job 2: pbip-docs        │
    (ubuntu-latest)       (DISABLED)              │
        │                     │                     │
    PBIXRay Engine        MCP Engine              │
        │                     (compatibility issue) │
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
- `**.pbip` - Any PBIP project file (⚠️ documentation disabled)
- `**.SemanticModel/**` - Any file in a SemanticModel folder (⚠️ documentation disabled)
- `.github/workflows/generate-wiki.yml` - Workflow itself

### Manual (Workflow Dispatch)
Run manually from GitHub Actions tab with options:
- **file_path**: Path to PBIX file or PBIP folder (⚠️ PBIP disabled)
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

**Runs when**: **DISABLED** - PBIP job currently disabled due to compatibility issues

**Known Issue**: The Microsoft MCP server executable (`powerbi-modeling-mcp.exe`) fails to start in GitHub Actions hosted runners with `WinError 216`, indicating missing system dependencies or runtime incompatibilities. Both .NET 8.0 and Visual C++ redistributables did not resolve the issue.

**Workarounds**:
1. Run PBIP documentation locally (works perfectly)
2. Export PBIP as PBIX and use the pbix-docs job
3. Use self-hosted Windows runner with proper dependencies

## File Detection Logic

### Push Events

**PBIX Job**:
- Detects changed `*.pbix` files via `git diff`
- Falls back to all PBIX files if none changed

**PBIP Job** (disabled):
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
- ❌ **DISABLED** - MCP server compatibility issues in GitHub Actions (WinError 216)
- ✅ Works perfectly for local execution
- ✅ Full metadata extraction when run locally
- ❌ GitHub Actions hosted runners missing required dependencies
- ❌ No Fabric remote connections (authentication issues)
- ⚠️ Self-hosted Windows runner may work (untested)

**PBIP Workarounds for CI/CD:**
1. Export PBIP as PBIX and commit for pbix-docs job
2. Run documentation locally and commit to docs/
3. Use self-hosted Windows runner (requires testing)

## Troubleshooting

### PBIX Job Fails
- Check Python dependencies in `requirements.txt`
- Verify pbixray-mcp-server installation
- Check PBIX file is not corrupted

### PBIP Job Disabled
The PBIP job is currently disabled due to Microsoft MCP server compatibility issues:

**Error**: `WinError 216: This version of %1 is not compatible with the version of Windows you're running`

**Cause**: The `powerbi-modeling-mcp.exe` requires system dependencies not available in GitHub Actions hosted Windows runners (Windows Server 2022).

**Attempted fixes** (unsuccessful):
- ✗ .NET 8.0 Runtime installation
- ✗ Visual C++ Redistributables
- ✗ Explicit windows-2022 runner

**Resolution**: Use local execution for PBIP documentation until Microsoft resolves compatibility issues.

### Both Jobs Run
Normal behavior when both PBIX and PBIP files change. Currently only pbix-docs will execute.

### No Commits
- Check if files actually changed
- Verify documentation wasn't already up-to-date
- Look for "No changes to commit" message

## Cost Considerations

### Linux Runner
- Free for public repos
- Fast execution (~2-3 minutes)

### Windows Runner (Disabled)
- Would be 2x multiplier for billing on private repos
- Would be slower execution (~5-8 minutes including MCP download)
- Currently disabled, no cost impact

## Future Enhancements

Potential improvements:
- **Fix PBIP job compatibility** - Work with Microsoft to resolve WinError 216
- Test self-hosted Windows runners for PBIP support
- Cache MCP server installation between runs (if PBIP re-enabled)
- Parallel PBIP folder processing
- Support for Fabric workspace connections (needs auth solution)
- Consolidated commit strategy (single commit for both jobs)
