"""
TOON (Token-Oriented Object Notation) Serializer Prototype
==========================================================

A lightweight implementation of TOON to demonstrate token savings.
TOON aims to reduce token usage by removing JSON syntax noise (braces, quotes, commas).

Reference: https://github.com/toon-format/toon (Conceptual)

Limitations:
- This is a prototype implementation for demonstration purposes
- Nested lists are serialized inline with brackets for better token efficiency
- Empty collections use compact notation
- No support for circular references or custom objects
"""

from typing import Any


class ToonSerializer:
    """
    Serializes and deserializes Python objects to/from TOON-like format.

    Format Rules (Simplified):
    - Keys and values separated by `: `
    - Indentation for nesting (2 spaces)
    - No quotes around keys or simple string values
    - No trailing commas
    - Lists denoted by `- ` or inline with brackets for nested structures
    - Empty collections use compact notation
    """

    @staticmethod
    def dumps(obj: Any, indent_level: int = 0) -> str:
        """
        Serialize object to TOON string.
        
        Args:
            obj: Object to serialize
            indent_level: Current indentation level (internal use)
            
        Returns:
            TOON formatted string
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
                return "~[]"  # Compact empty list notation
            
            # Check if all items are simple (non-nested) - if so, use inline format
            all_simple = all(not isinstance(item, (dict, list, tuple)) for item in obj)
            
            if all_simple:
                # Inline format for simple lists: [item1, item2, item3]
                items_str = ", ".join(ToonSerializer.dumps(item, 0) for item in obj)
                return f"[{items_str}]"
            
            # Multi-line format for complex lists
            lines = []
            for item in obj:
                if isinstance(item, (dict, list, tuple)):
                    # For nested structures, serialize inline if possible
                    item_str = ToonSerializer.dumps(item, 0)
                    if "\n" not in item_str:
                        # Can fit on one line
                        lines.append(f"{indent}- {item_str}")
                    else:
                        # Multi-line nested structure
                        lines.append(f"{indent}-")
                        lines.append(ToonSerializer.dumps(item, indent_level + 1))
                else:
                    formatted_item = ToonSerializer.dumps(item, 0)
                    lines.append(f"{indent}- {formatted_item}")
            return "\n".join(lines)

        if isinstance(obj, dict):
            if not obj:
                return "~{}"  # Compact empty dict notation
            lines = []
            for k, v in obj.items():
                if isinstance(v, (dict, list, tuple)):
                    # Check if value can be serialized inline
                    v_str = ToonSerializer.dumps(v, 0)
                    if "\n" not in v_str:
                        # Inline format
                        lines.append(f"{indent}{k}: {v_str}")
                    else:
                        # Multi-line format
                        lines.append(f"{indent}{k}:")
                        lines.append(ToonSerializer.dumps(v, indent_level + 1))
                else:
                    val_str = ToonSerializer.dumps(v, 0)
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

    @staticmethod
    def loads(toon_str: str) -> Any:
        """
        Deserialize TOON string to Python object.
        
        Args:
            toon_str: TOON formatted string
            
        Returns:
            Deserialized Python object
            
        Note:
            This is a simplified implementation that handles the basic TOON format.
            It may not handle all edge cases or complex nested structures.
        """
        return ToonSerializer._parse_value(toon_str.strip())

    @staticmethod
    def _parse_value(text: str) -> Any:
        """Parse a TOON value (internal helper)."""
        text = text.strip()
        
        if not text:
            return None
            
        # Handle literals
        if text == "null":
            return None
        if text == "true":
            return True
        if text == "false":
            return False
        if text == "~[]":
            return []  # Empty list
        if text == "~{}":
            return {}  # Empty dict
        if text == "~":
            return []  # Default to empty list for backward compatibility
            
        # Handle numbers
        try:
            if "." in text:
                return float(text)
            return int(text)
        except ValueError:
            pass
        
        # Handle quoted strings
        if text.startswith('"') and text.endswith('"'):
            import json
            return json.loads(text)
            
        # Handle inline lists: [item1, item2, item3]
        if text.startswith("[") and text.endswith("]"):
            inner = text[1:-1].strip()
            if not inner:
                return []
            # Simple comma split (doesn't handle nested brackets perfectly, but works for simple cases)
            items = []
            current = ""
            depth = 0
            for char in inner:
                if char in "[{":
                    depth += 1
                elif char in "]}":
                    depth -= 1
                elif char == "," and depth == 0:
                    items.append(ToonSerializer._parse_value(current.strip()))
                    current = ""
                    continue
                current += char
            if current.strip():
                items.append(ToonSerializer._parse_value(current.strip()))
            return items
        
        # Handle multi-line structures
        if "\n" in text:
            lines = text.split("\n")
            
            # Check if it's a list (lines start with -)
            has_list_items = any(line.strip().startswith("-") for line in lines if line.strip())
            has_dict_items = any(":" in line and not line.strip().startswith("-") for line in lines if line.strip())
            
            if has_list_items and not has_dict_items:
                return ToonSerializer._parse_list(lines)
            
            # Otherwise it's a dict
            return ToonSerializer._parse_dict(lines)
        
        # Check if it's a single-line key:value that wasn't parsed as dict
        if ":" in text and not text.startswith("-"):
            # This might be part of a dict structure
            lines = [text]
            return ToonSerializer._parse_dict(lines)
        
        # Plain string
        return text

    @staticmethod
    def _parse_list(lines: list[str]) -> list[Any]:
        """Parse a multi-line TOON list."""
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if not stripped or not stripped.startswith("-"):
                i += 1
                continue
                
            # Check if there's a value on the same line
            value_part = stripped[1:].strip()
            if value_part:
                result.append(ToonSerializer._parse_value(value_part))
                i += 1
            else:
                # Value is on next lines (nested structure)
                i += 1
                nested_lines = []
                base_indent = None
                while i < len(lines):
                    next_line = lines[i]
                    if not next_line.strip():
                        i += 1
                        continue
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if base_indent is None:
                        base_indent = next_indent
                    if next_indent < base_indent and next_line.strip():
                        break
                    nested_lines.append(next_line)
                    i += 1
                if nested_lines:
                    result.append(ToonSerializer._parse_value("\n".join(nested_lines)))
        
        return result

    @staticmethod
    def _parse_dict(lines: list[str]) -> dict[str, Any]:
        """Parse a multi-line TOON dict."""
        result = {}
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if not stripped:
                i += 1
                continue
            
            # Check if this is a list item (starts with -)
            if stripped.startswith("-"):
                # This is actually a list, not a dict
                return ToonSerializer._parse_list(lines)
            
            if ":" not in stripped:
                i += 1
                continue
            
            # Split on first colon
            key, _, value_part = stripped.partition(":")
            key = key.strip()
            value_part = value_part.strip()
            
            indent_level = len(line) - len(line.lstrip())
            
            if value_part:
                # Value on same line
                result[key] = ToonSerializer._parse_value(value_part)
                i += 1
            else:
                # Value on next lines (nested structure)
                i += 1
                nested_lines = []
                base_indent = None
                while i < len(lines):
                    next_line = lines[i]
                    if not next_line.strip():
                        i += 1
                        continue
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if base_indent is None:
                        base_indent = next_indent
                    # Check if we've reached a sibling key at the same level
                    if next_indent <= indent_level and ":" in next_line.strip():
                        break
                    nested_lines.append(next_line)
                    i += 1
                if nested_lines:
                    result[key] = ToonSerializer._parse_value("\n".join(nested_lines))
        
        return result

