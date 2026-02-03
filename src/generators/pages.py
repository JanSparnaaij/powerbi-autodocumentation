# src/generators/pages.py
from datetime import datetime
from ..mcp_client.pbixray_tools import Table, Measure, Relationship


def generate_home_page(
    model_name: str,
    summary: dict,
    tables: list[Table],
    measures: list[Measure]
) -> str:
    """Generate the wiki home page."""
    
    table_count = len(tables)
    measure_count = len(measures)
    
    # Build table of contents
    table_links = "\n".join(
        f"- [{t.name}](Table-{_slugify(t.name)}.md)"
        for t in tables
    )
    
    # Extract model size from summary with multiple field name attempts
    model_size = 'N/A'
    if isinstance(summary, dict):
        # Try various field names (PascalCase, snake_case, etc.)
        model_size = (summary.get('SizeBytes') or 
                      summary.get('size_bytes') or 
                      summary.get('ModelSize') or 
                      summary.get('model_size') or 
                      summary.get('Size') or 
                      summary.get('size') or 
                      'N/A')
    
    return f"""# {model_name} - Semantic Model Documentation

> Auto-generated on {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}

## Model Overview

| Metric | Value |
|--------|-------|
| Tables | {table_count} |
| Measures | {measure_count} |
| Model Size | {model_size} bytes |

## Quick Navigation

### Tables

{table_links}

### Other Pages

- [All Measures](Measures.md)
- [Relationships](Relationships.md)
- [Data Sources](Data-Sources.md)

---

This documentation is automatically generated from the PBIX file. For questions or issues, contact the BI team.
"""


def generate_table_page(
    table: Table,
    measures: list[Measure]
) -> str:
    """Generate a documentation page for a table."""
    
    # Build columns table
    columns_rows = []
    if table.columns:
        for col in table.columns:
            # Handle both dict and object column formats
            if isinstance(col, dict):
                col_name = col.get("Name") or col.get("name") or col.get("ColumnName") or ""
                col_type = col.get("DataType") or col.get("dataType") or col.get("data_type") or "Unknown"
                col_desc = col.get("Description") or col.get("description") or ""
            else:
                col_name = getattr(col, 'name', getattr(col, 'Name', ''))
                col_type = getattr(col, 'data_type', getattr(col, 'DataType', 'Unknown'))
                col_desc = getattr(col, 'description', getattr(col, 'Description', ''))
            
            # Escape pipe characters in descriptions
            col_desc = col_desc.replace("|", "\\|") if col_desc else ""
            columns_rows.append(f"| {col_name} | {col_type} | {col_desc} |")
    
    columns_table = "\n".join(columns_rows) if columns_rows else "| No columns available | | |"
    
    # Find measures in this table
    table_measures = [m for m in measures if m.table == table.name]
    measures_section = ""
    
    if table_measures:
        measures_rows = []
        for m in table_measures:
            # Clean expression: escape pipes, replace newlines with spaces, limit length
            if m.expression:
                expr = m.expression.replace("|", "\\|").replace("\n", " ").replace("\r", "")
                # Collapse multiple spaces
                expr = " ".join(expr.split())
                # Limit to 50 chars
                expr = expr[:50] + "..." if len(expr) > 50 else expr
            else:
                expr = ""
            measures_rows.append(f"| [{m.name}](Measures#{_slugify(m.name)}) | `{expr}` |")
        
        measures_section = f"""
## Measures

| Measure | Expression |
|---------|------------|
{chr(10).join(measures_rows)}
"""
    
    return f"""# Table: {table.name}

## Overview

**Row Count**: {table.row_count if table.row_count is not None else 'N/A'}

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
{columns_table}
{measures_section}

---

[← Back to Home](Home.md)
"""


def generate_measures_page(measures: list[Measure]) -> str:
    """Generate a page documenting all measures."""
    
    # Group measures by table
    measures_by_table = {}
    for m in measures:
        if m.table not in measures_by_table:
            measures_by_table[m.table] = []
        measures_by_table[m.table].append(m)
    
    content = f"""# All Measures

> Total Measures: {len(measures)}

"""
    
    for table_name in sorted(measures_by_table.keys()):
        content += f"\n## {table_name}\n\n"
        
        for m in measures_by_table[table_name]:
            content += f"### {m.name}\n\n"
            
            if m.description:
                content += f"**Description**: {m.description}\n\n"
            
            if m.format_string:
                content += f"**Format**: `{m.format_string}`\n\n"
            
            if m.display_folder:
                content += f"**Display Folder**: {m.display_folder}\n\n"
            
            content += f"""**Expression**:
```dax
{m.expression}
```

---

"""
    
    content += "\n[← Back to Home](Home.md)\n"
    return content


def generate_relationships_page(
    relationships: list[Relationship],
    er_diagram: str
) -> str:
    """Generate a page documenting relationships."""
    
    content = f"""# Relationships

> Total Relationships: {len(relationships)}

## Entity Relationship Diagram

```mermaid
{er_diagram}
```

## Relationship Details

| From Table | From Column | To Table | To Column | Active | Cross Filter |
|------------|-------------|----------|-----------|--------|--------------|
"""
    
    for r in relationships:
        active = "✓" if r.is_active else "✗"
        content += f"| {r.from_table} | {r.from_column} | {r.to_table} | {r.to_column} | {active} | {r.cross_filter_direction} |\n"
    
    content += "\n---\n\n[← Back to Home](Home.md)\n"
    return content


def generate_data_sources_page(power_query: str) -> str:
    """Generate a page documenting data sources and Power Query."""
    
    return f"""# Data Sources

## Power Query / M Code

The following Power Query code defines the data sources and transformations for this model:

```powerquery
{power_query}
```

---

[← Back to Home](Home.md)
"""


def _slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    return text.lower().replace(" ", "-").replace("_", "-")
