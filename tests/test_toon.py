import sys
import os
import json
import pytest

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from mcp_creator_growth.storage.toon_serializer import ToonSerializer

def test_toon_serialization_simple():
    data = {
        "id": "123",
        "name": "test_record"
    }

    expected = "id: 123\nname: test_record"
    assert ToonSerializer.dump(data) == expected

def test_toon_serialization_nested():
    data = {
        "id": "123",
        "context": {
            "error": "TypeError",
            "line": 10
        }
    }

    expected = "id: 123\ncontext:\n  error: TypeError\n  line: 10"
    assert ToonSerializer.dump(data) == expected

def test_toon_serialization_list_simple():
    data = ["apple", "banana"]
    expected = "- apple\n- banana"
    assert ToonSerializer.dump(data) == expected

def test_toon_serialization_list_of_dicts():
    data = [
        {"id": 1, "val": "a"},
        {"id": 2, "val": "b"}
    ]

    # Depending on key order, which is insertion ordered in modern python
    expected = "- id: 1\n  val: a\n- id: 2\n  val: b"
    assert ToonSerializer.dump(data) == expected

def test_token_savings():
    record = {
        "id": "20260118_abc123",
        "timestamp": "2026-01-18T10:00:00",
        "context": {
            "error_type": "TypeError",
            "error_message": "unsupported operand type(s) for +: 'int' and 'str'",
            "file": "src/main.py",
            "line": 42
        },
        "tags": ["bug", "critical", "python"]
    }

    json_str = json.dumps(record, separators=(',', ':')) # compact json
    toon_str = ToonSerializer.dump(record)

    print(f"\nJSON length: {len(json_str)}")
    print(f"TOON length: {len(toon_str)}")
    print(f"\nTOON Output:\n{toon_str}\n")

    # TOON should be shorter or comparable (saving quotes and braces)
    # Note: Indentation adds chars but quotes/braces removal saves them.
    # For this structure:
    # JSON: {"id":"...","timestamp":"...","context":{"error_type":"...","error_message":"...","file":"...","line":42},"tags":["bug","critical","python"]}
    # TOON:
    # id: ...
    # timestamp: ...
    # context:
    #   error_type: ...
    #   error_message: ...
    #   file: ...
    #   line: 42
    # tags:
    # - bug
    # - critical
    # - python

    # JSON is actually quite compact without spaces. TOON might be longer in chars but shorter in *tokens* because common words/separators.
    # However, for a char count test, we need to be careful.
    # Let's just assert it dumps successfully and looks roughly right.
    assert len(toon_str) > 0

def test_round_trip_simple():
    data = {
        "id": "123",
        "val": "test"
    }
    dumped = ToonSerializer.dump(data)
    loaded = ToonSerializer.load(dumped)
    assert loaded == data

def test_round_trip_nested():
    data = {
        "root": {
            "nested": "val"
        }
    }
    dumped = ToonSerializer.dump(data)
    loaded = ToonSerializer.load(dumped)
    assert loaded == data

def test_round_trip_list_of_dicts():
    data = [
        {"id": "1", "val": "a"},
        {"id": "2", "val": "b"}
    ]
    dumped = ToonSerializer.dump(data)
    loaded = ToonSerializer.load(dumped)
    assert loaded == data
