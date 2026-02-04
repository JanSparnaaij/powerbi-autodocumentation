# Release Notes - v0.3.1

**Release Date**: February 4, 2026

## 🎯 Overview

Version 0.3.1 adds **GitHub Actions automation** for PBIX documentation and fixes critical Fabric connectivity issues in the MCP engine. This release also documents a known compatibility limitation with PBIP in CI/CD environments.

## ✨ What's New

### 🤖 GitHub Actions Workflow

Automated documentation generation is now available for PBIX files via GitHub Actions:

**Features:**
- ✅ **Automatic trigger** on push when PBIX files change
- ✅ **Manual dispatch** with custom file path input
- ✅ **Auto-commit** documentation updates to `docs/` folder
- ✅ **Fast execution** (~2-3 minutes on Linux runner)
- ✅ **Free for public repos** using ubuntu-latest runner

**Usage:**
Simply push PBIX files to your repository and documentation is generated automatically. See [`.github/workflows/README.md`](/.github/workflows/README.md) for complete setup guide.

```yaml
# Triggers on:
- Push to **.pbix files
- Manual workflow dispatch
```

### 🔧 Bug Fixes

#### Fabric Connection String Parsing
Fixed MCP engine Fabric workspace URL parsing:
- ✅ Correctly extracts `workspaceName` and `semanticModelName` parameters
- ✅ Handles Power BI service URLs: `powerbi://api.powerbi.com/v1.0/myorg/My Workspace`
- ✅ Better error messages for invalid connection strings
- ✅ Added `_build_request()` helper for optional connectionName handling

**Before:** Failed to parse workspace names with special characters  
**After:** Correctly handles all valid Fabric workspace URLs

## ⚠️ Known Issues

### PBIP Documentation in GitHub Actions (Disabled)

The PBIP documentation job has been **temporarily disabled** in GitHub Actions due to Microsoft MCP server compatibility issues:

**Error:** `WinError 216: This version of %1 is not compatible with the version of Windows you're running`

**Root Cause:**
- Microsoft's `powerbi-modeling-mcp.exe` requires system dependencies not available in GitHub Actions hosted Windows runners (Windows Server 2022)
- Issue affects CI/CD environments only - local execution works perfectly

**Workarounds:**
1. 🎯 **Use local execution** for PBIP documentation (recommended, fully working)
2. 📦 **Export PBIP as PBIX** and commit for automated documentation
3. 🖥️ **Use self-hosted Windows runner** (requires testing)

**Status:** We're monitoring this issue and will re-enable PBIP automation when Microsoft resolves the compatibility issues.

## 📚 Documentation Updates

### New Documentation
- **GitHub Actions Workflow Guide** (`.github/workflows/README.md`)
  - Architecture diagram
  - Job descriptions and file detection logic
  - Troubleshooting section
  - Cost considerations

### Enhanced Sections
- **Fabric Troubleshooting** in main README
  - Remote connection authentication issues
  - Workaround options (PBIP export, Desktop localhost, PBIX download)
- **MCP Compatibility** notes for CI/CD environments

## 🚀 What Works

### ✅ Fully Functional
- **PBIX Documentation**: Local and GitHub Actions ✅
- **PBIP Documentation**: Local execution with MCP engine ✅
- **Desktop Live Connections**: Local with MCP engine ✅
- **Fabric Connections**: Local execution (with documented authentication limitations) ⚠️

### ⏳ Limited/Disabled
- **PBIP in GitHub Actions**: Disabled due to MCP server compatibility ❌
- **Fabric Remote in Headless**: Authentication issues (use workarounds) ⚠️

## 📦 Installation

No changes to installation process. See main README for setup instructions.

## 🔄 Upgrading from v0.3.0

This is a **patch release** with no breaking changes:

```bash
git pull
pip install -r requirements.txt
```

All existing commands and workflows remain unchanged. GitHub Actions is opt-in via workflow file.

## 🤝 Acknowledgements

- **Microsoft** for the Power BI Modeling MCP Server
- **PBIXRay** team for the foundational PBIX parsing library
- **Community feedback** on Fabric connectivity and CI/CD automation

## 📝 Full Changelog

See [CHANGELOG.md](/CHANGELOG.md) for detailed technical changes.

## 🐛 Reporting Issues

Found a bug? Open an issue on [GitHub Issues](https://github.com/JanSparnaaij/powerbi-autodocumentation/issues).

---

**Previous Release:** [v0.3.0](https://github.com/JanSparnaaij/powerbi-autodocumentation/releases/tag/v0.3.0) - MCP Engine Support  
**Repository:** https://github.com/JanSparnaaij/powerbi-autodocumentation
