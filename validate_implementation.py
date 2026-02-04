"""Validation script for MCP engine implementation.

This script performs comprehensive checks to ensure the MCP engine
implementation is correct and production-ready.
"""

import sys
import asyncio
from pathlib import Path


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def check_imports():
    """Check that all modules can be imported."""
    print_section("Module Import Checks")
    
    try:
        from src.engines import (
            IDocumentationEngine,
            ModelMetadata,
            get_engine,
            list_engines,
            register_engine,
        )
        print("✓ Engine abstraction imports successful")
    except ImportError as e:
        print(f"✗ Engine abstraction import failed: {e}")
        return False
    
    try:
        from src.engines.pbixray import PBIXRayEngine
        print("✓ PBIXRay engine imports successful")
    except ImportError as e:
        print(f"✗ PBIXRay engine import failed: {e}")
        return False
    
    try:
        from src.engines.mcp import (
            ModelingMCPEngine,
            MCPEngineConfig,
            MCPMode,
            find_powerbi_mcp_server,
            validate_server_path,
        )
        print("✓ MCP engine imports successful")
    except ImportError as e:
        print(f"✗ MCP engine import failed: {e}")
        return False
    
    return True


def check_engine_registry():
    """Check engine registry functionality."""
    print_section("Engine Registry Checks")
    
    from src.engines import list_engines, get_engine
    
    # Check available engines
    engines = list_engines()
    print(f"Available engines: {', '.join(engines)}")
    
    if "pbixray" not in engines:
        print("✗ pbixray engine not registered")
        return False
    print("✓ pbixray engine registered")
    
    if "mcp" not in engines:
        print("✗ mcp engine not registered")
        return False
    print("✓ mcp engine registered")
    
    # Check engine creation
    try:
        pbixray_engine = get_engine("pbixray")
        print(f"✓ pbixray engine instantiation: {type(pbixray_engine).__name__}")
    except Exception as e:
        print(f"✗ pbixray engine instantiation failed: {e}")
        return False
    
    try:
        mcp_engine = get_engine("mcp")
        print(f"✓ mcp engine instantiation: {type(mcp_engine).__name__}")
    except Exception as e:
        print(f"✗ mcp engine instantiation failed: {e}")
        return False
    
    return True


def check_mcp_config():
    """Check MCP configuration."""
    print_section("MCP Configuration Checks")
    
    from src.engines.mcp import MCPEngineConfig, MCPMode
    
    # Test default config
    config = MCPEngineConfig()
    print(f"Default mode: {config.mode}")
    print(f"Default timeout: {config.timeout}")
    print(f"Default retries: {config.max_retries}")
    
    if config.mode != MCPMode.READONLY:
        print("✗ Default mode should be READONLY")
        return False
    print("✓ Default mode is READONLY")
    
    # Test server args
    args = config.get_server_args()
    print(f"Server args: {args}")
    
    if "--readonly" not in args:
        print("✗ --readonly not in default server args")
        return False
    print("✓ --readonly in server args")
    
    if "--start" not in args:
        print("✗ --start not in default server args")
        return False
    print("✓ --start in server args")
    
    # Test readwrite mode
    config_rw = MCPEngineConfig(mode=MCPMode.READWRITE)
    args_rw = config_rw.get_server_args()
    
    if "--readwrite" not in args_rw:
        print("✗ --readwrite not in readwrite mode args")
        return False
    print("✓ --readwrite in readwrite mode args")
    
    return True


def check_mcp_discovery():
    """Check MCP server discovery."""
    print_section("MCP Discovery Checks")
    
    from src.engines.mcp import find_powerbi_mcp_server, validate_server_path
    
    # Test validation with non-existent path
    result = validate_server_path("C:\\nonexistent\\server.exe")
    if result:
        print("✗ validate_server_path should return False for non-existent path")
        return False
    print("✓ Validation rejects non-existent paths")
    
    # Test server discovery
    server_path = find_powerbi_mcp_server()
    if server_path:
        print(f"✓ MCP server found: {server_path}")
    else:
        print("⚠ MCP server not found (expected if not installed)")
        print("  Set POWERBI_MCP_PATH or install Power BI VS Code extension")
    
    return True


def check_cli():
    """Check CLI functionality."""
    print_section("CLI Checks")
    
    import subprocess
    
    # Test help output
    try:
        result = subprocess.run(
            ["python", "generate_wiki.py", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        help_text = result.stdout
        
        required_options = [
            "--engine",
            "--pbip",
            "--desktop",
            "--mcp-mode",
            "--mcp-timeout",
            "--verbose",
        ]
        
        missing = []
        for option in required_options:
            if option not in help_text:
                missing.append(option)
        
        if missing:
            print(f"✗ Missing CLI options: {', '.join(missing)}")
            return False
        
        print(f"✓ All required CLI options present")
        
        if "pbixray,mcp" in help_text or "{pbixray,mcp}" in help_text:
            print("✓ Engine choices displayed correctly")
        else:
            print("⚠ Engine choices may not be displayed correctly")
        
        return True
    
    except Exception as e:
        print(f"✗ CLI check failed: {e}")
        return False


def check_file_structure():
    """Check that all expected files exist."""
    print_section("File Structure Checks")
    
    required_files = [
        "src/engines/__init__.py",
        "src/engines/base.py",
        "src/engines/registry.py",
        "src/engines/pbixray/__init__.py",
        "src/engines/pbixray/engine.py",
        "src/engines/mcp/__init__.py",
        "src/engines/mcp/engine.py",
        "src/engines/mcp/config.py",
        "src/engines/mcp/discovery.py",
        "tests/engines/test_registry.py",
        "tests/engines/test_discovery.py",
        "examples/mcp/README.md",
        "examples/mcp/document_pbip.py",
        "examples/mcp/document_desktop.py",
        "CHANGELOG.md",
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print("✗ Missing files:")
        for file_path in missing:
            print(f"  - {file_path}")
        return False
    
    print(f"✓ All {len(required_files)} required files present")
    return True


def check_tests():
    """Run the test suite."""
    print_section("Test Suite Checks")
    
    import subprocess
    
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/engines/", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout + result.stderr
        
        if "passed" in output:
            # Extract passed count
            import re
            match = re.search(r'(\d+) passed', output)
            if match:
                passed_count = int(match.group(1))
                print(f"✓ {passed_count} tests passed")
        
        if result.returncode != 0:
            print("✗ Some tests failed")
            print(output)
            return False
        
        return True
    
    except Exception as e:
        print(f"✗ Test execution failed: {e}")
        return False


def main():
    """Run all validation checks."""
    print("\n" + "="*60)
    print("  MCP ENGINE IMPLEMENTATION VALIDATION")
    print("="*60)
    
    checks = [
        ("Module Imports", check_imports),
        ("Engine Registry", check_engine_registry),
        ("MCP Configuration", check_mcp_config),
        ("MCP Discovery", check_mcp_discovery),
        ("File Structure", check_file_structure),
        ("CLI Functionality", check_cli),
        ("Test Suite", check_tests),
    ]
    
    results = {}
    
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n✗ {name} check crashed: {e}")
            results[name] = False
    
    # Print summary
    print_section("VALIDATION SUMMARY")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All validation checks passed!")
        print("✓ Implementation is production-ready")
        return 0
    else:
        print(f"\n⚠ {total - passed} validation check(s) failed")
        print("✗ Please review and fix issues above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
