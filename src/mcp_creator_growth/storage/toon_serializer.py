"""
TOON (Token-Oriented Object Notation) Serializer Prototype
==========================================================

A lightweight implementation of TOON to demonstrate token savings.
TOON aims to reduce token usage by removing JSON syntax noise (braces, quotes, commas).

Reference: https://github.com/toon-format/toon (Conceptual)
"""

from typing import Any


class ToonSerializer:
    """
    Serializes Python objects to TOON-like format.

    Format Rules (Simplified):
    - Keys and values separated by `: `
    - Indentation for nesting (2 spaces)
    - No quotes around keys or simple string values
    - No trailing commas
    - Lists denoted by `- `
    """

    @staticmethod
    def dumps(obj: Any, indent_level: int = 0) -> str:
        """
        Serialize object to TOON string.
        """
        indent = "  " * indent_level

        if obj is None:
            return "null"

        if isinstance(obj, bool):
            return "true" if obj else "false"

        if isinstance(obj, (int, float)):
            return str(obj)

        if isinstance(obj, str):
            # Check if string needs quoting (if it contains special chars or newlines)
            if "\n" in obj or ":" in obj or obj.startswith("- ") or obj == "" or '"' in obj:
                # Use Python's repr to safely handle escaping
                import json
                return json.dumps(obj)
            return obj

        if isinstance(obj, (list, tuple)):
            if not obj:
                return "[]"
            lines = []
            for item in obj:
                # If item is complex, it needs its own line and indent
                # If item is simple, it can be inline?
                # TOON usually does:
                # - item1
                # - item2
                formatted_item = ToonSerializer.dumps(item, indent_level + 1).strip()
                if isinstance(item, (dict, list, tuple)):
                     # For complex types, we need to handle the first line carefully
                     # simplistic approach:
                     lines.append(f"{indent}-")
                     lines.append(ToonSerializer.dumps(item, indent_level + 1))
                else:
                    lines.append(f"{indent}- {formatted_item}")
            return "\n".join(lines)

        if isinstance(obj, dict):
            if not obj:
                return "{}"
            lines = []
            for k, v in obj.items():
                if isinstance(v, (dict, list, tuple)):
                    lines.append(f"{indent}{k}:")
                    lines.append(ToonSerializer.dumps(v, indent_level + 1))
                else:
                    val_str = ToonSerializer.dumps(v, indent_level + 1).strip()
                    lines.append(f"{indent}{k}: {val_str}")
            return "\n".join(lines)

        return str(obj)

    @staticmethod
    def estimate_token_savings(json_str: str, toon_str: str) -> float:
        """
        Estimate token savings based on character count (rough proxy).
        Real tokenizers are more complex, but char count is a good heuristic.
        """
        json_len = len(json_str)
        toon_len = len(toon_str)
        if json_len == 0:
            return 0.0
        return (json_len - toon_len) / json_len * 100.0
