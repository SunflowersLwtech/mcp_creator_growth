"""
Serializers
===========

JSON serialization and deserialization utilities for storage.
Handles sessions, debug records, and metadata.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..debug import server_debug_log as debug_log


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Path):
            return str(obj)
        return super().default(obj)


def serialize_to_json(data: dict[str, Any], pretty: bool = False) -> str:
    """
    Serialize data to JSON string.

    Args:
        data: Data to serialize
        pretty: If True, format with indentation (default: False for compactness)

    Returns:
        JSON string
    """
    indent = 2 if pretty else None
    return json.dumps(
        data,
        cls=DateTimeEncoder,
        ensure_ascii=False,
        indent=indent,
    )


def deserialize_from_json(json_str: str) -> dict[str, Any]:
    """
    Deserialize JSON string to data.

    Args:
        json_str: JSON string to parse

    Returns:
        Parsed data dictionary

    Raises:
        json.JSONDecodeError: If JSON is invalid
    """
    return json.loads(json_str)


def save_json_file(
    file_path: Path | str,
    data: dict[str, Any],
    pretty: bool = False,
) -> None:
    """
    Save data to a JSON file.

    Args:
        file_path: Path to save the file
        data: Data to save
        pretty: If True, format with indentation (default: False for compactness)
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            cls=DateTimeEncoder,
            ensure_ascii=False,
            indent=2 if pretty else None,
        )

    debug_log(f"Saved JSON file: {file_path}")


def load_json_file(file_path: Path | str) -> dict[str, Any] | None:
    """
    Load data from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Loaded data or None if file doesn't exist
    """
    file_path = Path(file_path)

    if not file_path.exists():
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        debug_log(f"Error parsing JSON file {file_path}: {e}")
        return None
    except IOError as e:
        debug_log(f"Error reading file {file_path}: {e}")
        return None


def serialize_to_toon(data: dict[str, Any] | list[Any]) -> str:
    """
    Serialize data to TOON (Token-Oriented Object Notation) format.
    This is a simplified implementation focusing on token reduction via indentation.

    Args:
        data: Data to serialize

    Returns:
        TOON formatted string
    """
    def _to_toon_val(val: Any) -> str:
        if isinstance(val, (str, Path)):
            # Minimal escaping, assuming mostly code/text friendly
            s = str(val)
            if "\n" in s or ":" in s or "#" in s:
                return json.dumps(s)  # Fallback to JSON string for complex chars
            return s
        if isinstance(val, datetime):
            return val.isoformat()
        if val is None:
            return "null"
        if isinstance(val, bool):
            return "true" if val else "false"
        return str(val)

    def _recurse(obj: Any, level: int = 0) -> list[str]:
        indent = "  " * level
        lines = []

        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    lines.append(f"{indent}{k}:")
                    lines.extend(_recurse(v, level + 1))
                else:
                    lines.append(f"{indent}{k}: {_to_toon_val(v)}")
        elif isinstance(obj, list):
            # Check if it's a list of primitives (compact) or objects (expanded)
            if obj and all(not isinstance(x, (dict, list)) for x in obj):
                # Compact array style: [val, val, val] but without brackets if possible
                # For TOON, we might just use CSV-like or simple list
                # Simplified: use - bullet points for lists
                for item in obj:
                    lines.append(f"{indent}- {_to_toon_val(item)}")
            else:
                for item in obj:
                    lines.append(f"{indent}-")
                    lines.extend(_recurse(item, level + 1))
        return lines

    return "\n".join(_recurse(data))


def serialize_session(session_data: dict[str, Any]) -> dict[str, Any]:
    """
    Serialize a session for storage.

    Converts internal session data to storage format.

    Args:
        session_data: Session data to serialize

    Returns:
        Serialized session data
    """
    serialized = {
        "version": 1,
        "serialized_at": datetime.now().isoformat(),
    }

    # Copy all session fields
    for key, value in session_data.items():
        if isinstance(value, datetime):
            serialized[key] = value.isoformat()
        elif isinstance(value, Path):
            serialized[key] = str(value)
        else:
            serialized[key] = value

    return serialized


def deserialize_session(data: dict[str, Any]) -> dict[str, Any]:
    """
    Deserialize a session from storage.

    Converts storage format back to internal format.

    Args:
        data: Stored session data

    Returns:
        Deserialized session data
    """
    # Remove metadata fields
    result = {}
    for key, value in data.items():
        if key in ("version", "serialized_at"):
            continue
        result[key] = value

    return result


def merge_data(
    existing: dict[str, Any],
    new: dict[str, Any],
    overwrite: bool = True,
) -> dict[str, Any]:
    """
    Merge two data dictionaries.

    Args:
        existing: Existing data
        new: New data to merge
        overwrite: If True, new values overwrite existing

    Returns:
        Merged data
    """
    result = existing.copy()

    for key, value in new.items():
        if key not in result or overwrite:
            result[key] = value
        elif isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge dicts
            result[key] = merge_data(result[key], value, overwrite)
        elif isinstance(result[key], list) and isinstance(value, list):
            # Extend lists
            result[key] = result[key] + value

    return result
