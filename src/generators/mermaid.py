# src/generators/mermaid.py
from ..mcp_client.pbixray_tools import Relationship


def generate_er_diagram(
    relationships: list[Relationship],
    tables: list[str]
) -> str:
    """Generate Mermaid ER diagram from relationships."""
    lines = ["erDiagram"]
    
    # Track which tables are connected
    connected_tables = set()
    
    for rel in relationships:
        # Skip relationships with missing table names
        if not rel.from_table or not rel.to_table:
            print(f"Warning: Skipping relationship with empty table name: from='{rel.from_table}' to='{rel.to_table}'")
            continue
        
        connected_tables.add(rel.from_table)
        connected_tables.add(rel.to_table)
        
        # Determine cardinality notation
        # Power BI uses many-to-one as default
        cardinality = "||--o{" if rel.is_active else "||..o{"
        
        lines.append(
            f'    {_sanitize_name(rel.to_table)} '
            f'{cardinality} '
            f'{_sanitize_name(rel.from_table)} : '
            f'"{rel.from_column}"'
        )
    
    # Add disconnected tables
    for table in tables:
        if table not in connected_tables:
            lines.append(f'    {_sanitize_name(table)} {{')
            lines.append(f'        string placeholder')
            lines.append(f'    }}')
    
    return "\n".join(lines)


def _sanitize_name(name: str) -> str:
    """Sanitize table name for use in Mermaid diagrams."""
    # Replace spaces and special characters
    sanitized = name.replace(" ", "_").replace("-", "_")
    # Remove other problematic characters
    sanitized = "".join(c for c in sanitized if c.isalnum() or c == "_")
    return sanitized
