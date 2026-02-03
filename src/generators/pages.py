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
    
    return f"""# {model_name} - Semantic Model Documentation

> Auto-generated on {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}

## Model Overview

| Metric | Value |
|--------|-------|
| Tables | {table_count} |
| Measures | {measure_count} |
| Model Size | {summary.get('size_bytes', 'N/A') if isinstance(summary, dict) else 'N/A'} bytes |

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
    schema: dict,
    measures: list[Measure]
) -> str:
    """Generate a documentation page for a table."""
    
    # Build columns table
    columns_rows = []
    for col in table.columns:
        col_name = col.get("name", "")
        col_type = col.get("dataType", "Unknown")
        col_desc = col.get("description", "")
        # Escape pipe characters in descriptions
        col_desc = col_desc.replace("|", "\\|") if col_desc else ""
        columns_rows.append(f"| {col_name} | {col_type} | {col_desc} |")
    
    columns_table = "\n".join(columns_rows)
    
    # Find measures in this table
    table_measures = [m for m in measures if m.table == table.name]
    measures_section = ""
    
    if table_measures:
        measures_rows = []
        for m in table_measures:
            # Escape pipe characters in expressions
            expr = m.expression.replace("|", "\\|") if m.expression else ""
            measures_rows.append(f"| [{m.name}](Measures#{_slugify(m.name)}) | `{expr[:50]}...` |")
        
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

## Source Query

```powerquery
{schema.get('source_query', 'N/A')}
```

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
