"""
TOON Serializer (Prototype)
===========================

Token-Oriented Object Notation serializer.
Optimized for LLM context efficiency, particularly for tabular data.
"""

from typing import Any, List, Dict

def _escape(s: str) -> str:
    """Minimal escaping for pipe delimiter."""
    if s is None:
        return ""
    return str(s).replace("|", "||").replace("\n", "\\n")

def _unescape(s: str) -> str:
    return s.replace("\\n", "\n").replace("||", "|")

def dumps_table(data: List[Dict[str, Any]], keys: List[str] | None = None) -> str:
    """
    Serialize list of dicts to TOON Table format.

    Format:
    key1 | key2 | key3
    val1 | val2 | val3

    Args:
        data: List of dictionaries to serialize
        keys: Optional list of keys to include (determines column order)

    Returns:
        String in TOON table format
    """
    if not data:
        return ""

    if keys is None:
        # Infer keys from first item, but try to find all unique keys across items
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
        # Sort for deterministic output, but prioritize 'id'
        keys = sorted(list(all_keys))
        if "id" in keys:
            keys.remove("id")
            keys.insert(0, "id")

    lines = []
    # Header
    lines.append(" | ".join(keys))

    # Rows
    for item in data:
        values = []
        for k in keys:
            val = item.get(k, "")
            if isinstance(val, list):
                # Simple CSV-style list within a cell
                val = ", ".join(str(v) for v in val)
            values.append(_escape(str(val)))
        lines.append(" | ".join(values))

    return "\n".join(lines)

def loads_table(text: str) -> List[Dict[str, Any]]:
    """
    Deserialize TOON Table format.

    Args:
        text: String in TOON table format

    Returns:
        List of dictionaries
    """
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    if not lines:
        return []

    # Header
    keys = [k.strip() for k in lines[0].split("|")]
    result = []

    for line in lines[1:]:
        # Note: This simple split fails if values contain " | ".
        # A robust parser would scan char by char, but for this prototype
        # we assume values don't contain the delimiter sequence " | "
        # or we rely on the implementation matching `dumps_table`.
        parts = line.split(" | ")

        # If split count doesn't match keys, it might be due to empty trailing columns or bad formatting
        # We try to align as best as possible.

        item = {}
        for i, k in enumerate(keys):
            if i < len(parts):
                val = _unescape(parts[i].strip())
                # Heuristic for lists: if key implies list or val looks like list
                if "," in val and k in ["tags", "keywords", "categories"]:
                     # Only split if it's not empty
                     if val:
                        val = [v.strip() for v in val.split(",")]
                     else:
                        val = []
                item[k] = val
        result.append(item)

    return result
