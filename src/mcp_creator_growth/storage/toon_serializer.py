"""
TOON Serializer (Prototype)
===========================

Implements Token-Oriented Object Notation (TOON) serialization.
TOON is a compact, human-readable format designed to minimize token usage
for LLM context injection.

Format Rules:
- No quotes around keys (unless necessary)
- Indentation-based hierarchy (no braces)
- No trailing commas
- Minimal whitespace
"""

from typing import Any


class ToonSerializer:
    """
    Serializer for Token-Oriented Object Notation.
    """

    @staticmethod
    def serialize(data: Any, indent_level: int = 0) -> str:
        """
        Serialize data to TOON format.

        Args:
            data: The data to serialize (dict, list, str, int, bool, None)
            indent_level: Current indentation level (internal use)

        Returns:
            String representation in TOON format
        """
        indent = "  " * indent_level

        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                # optimize: if value is simple, keep on same line
                if isinstance(value, (str, int, float, bool, type(None))):
                    serialized_val = ToonSerializer._serialize_simple(value)
                    lines.append(f"{indent}{key}: {serialized_val}")
                else:
                    lines.append(f"{indent}{key}:")
                    lines.append(ToonSerializer.serialize(value, indent_level + 1))
            return "\n".join(lines)

        elif isinstance(data, list):
            lines = []
            for item in data:
                if isinstance(item, (str, int, float, bool, type(None))):
                    lines.append(f"{indent}- {ToonSerializer._serialize_simple(item)}")
                else:
                    lines.append(f"{indent}-")
                    lines.append(ToonSerializer.serialize(item, indent_level + 1))
            return "\n".join(lines)

        else:
            return f"{indent}{ToonSerializer._serialize_simple(data)}"

    @staticmethod
    def _serialize_simple(value: Any) -> str:
        """Helper to serialize simple values."""
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, str):
            # Quote strings only if they contain special chars or look like numbers/bools
            # For this prototype, we'll be safe and quote if it has spaces
            if " " in value or ":" in value or "\n" in value:
                # Basic escaping
                cleaned = value.replace('"', '\\"').replace('\n', '\\n')
                return f'"{cleaned}"'
            return value
        return str(value)

    @staticmethod
    def deserialize(toon_str: str) -> Any:
        """
        Deserialize TOON string to Python object.

        Note: This is a prototype parser and may not handle all edge cases.
        For production, use a dedicated TOON parsing library.
        """
        raise NotImplementedError("TOON deserialization not yet implemented for production use.")
