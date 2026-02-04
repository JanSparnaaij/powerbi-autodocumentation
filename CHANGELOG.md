# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2026-02-04

### Added
- **GitHub Actions Workflow**: Automated documentation generation for PBIX files
  - Hybrid workflow architecture with Linux runner for PBIX processing
  - Automatic trigger on PBIX/PBIP file changes
  - Manual workflow dispatch with file path input
  - Auto-commit documentation updates to `docs/` folder
  - Comprehensive workflow documentation in `.github/workflows/README.md`

### Fixed
- **Fabric Connection Parsing**: Fixed MCP engine connection string parsing for Fabric workspaces
  - Correctly extracts `workspaceName` and `semanticModelName` parameters
  - Improved error messages for invalid Fabric URLs
  - Added helper method `_build_request()` for optional connectionName handling

### Known Issues
- **PBIP in GitHub Actions**: PBIP documentation job disabled due to Microsoft MCP server compatibility
  - `WinError 216`: MCP server executable incompatible with GitHub Actions Windows runners
  - Root cause: Missing system dependencies in hosted Windows Server 2022 runners
  - Workaround: Use local execution for PBIP, or export as PBIX for CI/CD
  - Works perfectly: Local PBIP documentation with MCP engine

### Documentation
- Added GitHub Actions workflow guide with architecture diagram
- Documented MCP server WinError 216 compatibility issues
- Added PBIP CI/CD workarounds in workflow README
- Updated main README with Fabric troubleshooting section

## [0.3.0] - 2026-02-04

### Added - MCP Modeling Engine Support

**Major Feature**: Optional Power BI Modeling MCP engine integration (100% backward compatible)

#### New Features
- **Engine Abstraction Layer**: Pluggable architecture supporting multiple documentation engines
  - `IDocumentationEngine` interface for consistent metadata extraction
  - Engine registry and factory pattern for dynamic engine selection
  - Full backward compatibility - existing pbixray workflows unchanged

- **MCP Modeling Engine** (`--engine mcp`):
  - PBIP folder support (TMDL format) via `--pbip` flag
  - Power BI Desktop live connections via `--desktop` flag
  - Analysis Services connections
  - Auto-discovery from POWERBI_MCP_PATH or VS Code extension
  - Read-only (default) and read-write modes
  - Configurable timeout and retry logic
  - Feature detection for available MCP tools

- **New CLI Options**:
  ```bash
  --engine {pbixray,mcp}       # Choose documentation engine
  --pbip FOLDER                # Shortcut for PBIP folders
  --desktop CONNECTION         # Shortcut for Desktop connections
  --mcp-server PATH            # Custom MCP server path
  --mcp-mode {readonly,readwrite}
  --mcp-timeout SECONDS
  --mcp-retries COUNT
  --verbose                    # Enable debug logging
  ```

#### New Modules
- `src/engines/` - Engine abstraction layer
  - `base.py` - IDocumentationEngine interface, ModelMetadata container
  - `registry.py` - Engine factory and registration system
  - `pbixray/engine.py` - PBIXRay engine wrapper (backward compatible)
  - `mcp/engine.py` - Power BI Modeling MCP engine
  - `mcp/config.py` - MCP configuration dataclasses
  - `mcp/discovery.py` - Auto-discovery utilities

#### Tests
- 27 comprehensive unit tests for engine system:
  - Engine registry and factory tests
  - MCP server discovery tests
  - MCP configuration tests
  - Custom engine registration tests

#### Examples
- `examples/mcp/document_pbip.py` - PBIP folder documentation example
- `examples/mcp/document_desktop.py` - Desktop live connection example
- `examples/mcp/README.md` - Comprehensive MCP usage guide

#### Documentation
- Updated README with MCP engine section
- Engine comparison table
- Prerequisites and installation guide
- Complete usage examples for all scenarios
- Troubleshooting guide

### Changed
- **WikiGenerator** refactored to use engine abstraction (non-breaking)
- **CLI** renamed `pbix_file` arg to `source` (supports multiple source types)
- Logging enhanced throughout (uses Python `logging` module)
- Error messages more descriptive with troubleshooting hints

### Technical Details
- **Backward Compatibility**: ✅ 100% maintained
  - Default engine remains `pbixray`
  - Existing scripts work without modification
  - No breaking API changes
- **Production Grade**: 
  - Async/await throughout
  - Proper resource cleanup (context managers)
  - Retry logic with exponential backoff
  - Comprehensive error handling
  - Feature detection (no hardcoded tool assumptions)

### Migration Guide
No migration needed! All existing code continues to work:
```bash
# Existing usage - still works exactly the same
python generate_wiki.py model.pbix -o ./docs

# New capabilities - opt-in via flags
python generate_wiki.py --pbip ./model.Dataset -o ./docs
python generate_wiki.py --desktop localhost:51174 -o ./docs
```

## [0.2.0] - 2026-01-XX

### Added
- Multi-model support with per-model subfolders
- Index page listing all documented models
- PBIP detection (skips with warning as pbixray doesn't support)

### Changed
- Default branch changed from `master` to `main`
- Output structure: `docs/{model-slug}/` instead of flat `docs/`

### Fixed
- Relationship field name casing (FromTableName, ToTableName, CrossFilteringBehavior)
- Measure expression formatting (proper multiline DAX)
- Column schema parsing (PascalCase field names)
- Auto-date table handling (LocalDateTable relationships)
- Pandas StringArray in table string representations

## [0.1.0] - 2026-01-XX

### Added
- Initial release
- PBIX file documentation via pbixray-mcp-server
- GitHub Actions workflow automation
- Markdown page generation (Home, Tables, Measures, Relationships, Data Sources)
- Mermaid ER diagram generation
- Multi-table support
- Power Query code extraction

[0.3.0]: https://github.com/yourusername/powerbi-autodocumentation/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/yourusername/powerbi-autodocumentation/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/yourusername/powerbi-autodocumentation/releases/tag/v0.1.0
