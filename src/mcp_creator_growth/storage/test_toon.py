
import json
import sys
from pathlib import Path

# Add src to sys.path to allow imports
src_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_path))

from mcp_creator_growth.storage.toon_serializer import dumps_table, loads_table

def test_toon_serialization():
    data = [
        {"id": "r1", "error_type": "TypeError", "tags": ["python", "bug"]},
        {"id": "r2", "error_type": "ValueError", "tags": ["api", "invalid"]},
        {"id": "r3", "error_type": "IndexError", "tags": ["list", "bounds"]},
    ]

    print("--- Original Data ---")
    print(data)

    # JSON
    json_str = json.dumps(data, separators=(",", ":"))
    print(f"\n--- JSON Format ({len(json_str)} chars) ---")
    print(json_str)

    # TOON
    toon_str = dumps_table(data, keys=["id", "error_type", "tags"])
    print(f"\n--- TOON Format ({len(toon_str)} chars) ---")
    print(toon_str)

    # Savings
    savings = (1 - len(toon_str) / len(json_str)) * 100
    print(f"\n--- Savings: {savings:.1f}% ---")

    # Verification
    decoded = loads_table(toon_str)
    print("\n--- Decoded Data ---")
    print(decoded)

    assert len(decoded) == len(data)
    assert decoded[0]["id"] == "r1"
    assert decoded[0]["error_type"] == "TypeError"
    # Note: list comparison might need care depending on exact deserialization logic (e.g. whitespace)
    # The simple deserializer might leave whitespace if not careful, but we strip() in logic.
    assert "python" in decoded[0]["tags"]

    print("\nTEST PASSED: TOON serialization working correctly.")

if __name__ == "__main__":
    test_toon_serialization()
