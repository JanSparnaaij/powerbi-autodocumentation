"""Utility functions for markdown formatting"""


def escape_markdown(text: str) -> str:
    """Escape special characters in markdown text."""
    if not text:
        return ""
    
    # Escape pipe characters for tables
    text = text.replace("|", "\\|")
    
    # Escape backticks
    text = text.replace("`", "\\`")
    
    return text


def format_code_block(code: str, language: str = "") -> str:
    """Format code as a markdown code block."""
    return f"```{language}\n{code}\n```"


def create_table(headers: list[str], rows: list[list[str]]) -> str:
    """Create a markdown table."""
    if not headers or not rows:
        return ""
    
    # Build header
    header_row = "| " + " | ".join(headers) + " |"
    separator = "|" + "|".join(["-" * (len(h) + 2) for h in headers]) + "|"
    
    # Build rows
    data_rows = []
    for row in rows:
        data_rows.append("| " + " | ".join(str(cell) for cell in row) + " |")
    
    return "\n".join([header_row, separator] + data_rows)
