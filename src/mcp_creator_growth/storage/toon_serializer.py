"""
TOON (Token-Oriented Object Notation) Serializer.

Optimizes token usage for lists of objects by using a pipe-delimited table format.
"""

from typing import Any, Sequence

class ToonSerializer:
    """Serializer for TOON format."""

    @staticmethod
    def to_toon(data: Sequence[dict[str, Any]], headers: Sequence[str] | None = None) -> str:
        """
        Convert a list of dictionaries to TOON format string.

        Args:
            data: List of dictionaries to serialize.
            headers: Optional list of headers. If None, keys from the first item are used.

        Returns:
            String in TOON format (header row + pipe-delimited data rows).
        """
        if not data:
            return ""

        # If headers not provided, infer from first item keys
        if not headers:
            headers = list(data[0].keys())

        lines = []
        # Header row
        lines.append("|".join(headers))

        # Data rows
        for item in data:
            row = []
            for key in headers:
                val = item.get(key, "")
                # Basic escaping for pipe characters: replace with forward slash
                val_str = str(val).replace("|", "/")
                # Remove newlines to keep one record per line
                val_str = val_str.replace("\n", " ").replace("\r", "")
                row.append(val_str)
            lines.append("|".join(row))

        return "\n".join(lines)
