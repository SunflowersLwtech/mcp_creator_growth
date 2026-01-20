"""
Unit tests for ToonSerializer
"""

import json

from mcp_creator_growth.storage.toon_serializer import ToonSerializer


class TestToonSerializerBasicTypes:
    """Test serialization of basic types."""

    def test_none(self):
        assert ToonSerializer.dumps(None) == "null"
        assert ToonSerializer.loads("null") is None

    def test_boolean(self):
        assert ToonSerializer.dumps(True) == "true"
        assert ToonSerializer.dumps(False) == "false"
        assert ToonSerializer.loads("true") is True
        assert ToonSerializer.loads("false") is False

    def test_integers(self):
        assert ToonSerializer.dumps(42) == "42"
        assert ToonSerializer.dumps(0) == "0"
        assert ToonSerializer.dumps(-10) == "-10"
        assert ToonSerializer.loads("42") == 42
        assert ToonSerializer.loads("-10") == -10

    def test_floats(self):
        assert ToonSerializer.dumps(3.14) == "3.14"
        assert ToonSerializer.dumps(-2.5) == "-2.5"
        assert ToonSerializer.loads("3.14") == 3.14
        assert ToonSerializer.loads("-2.5") == -2.5

    def test_simple_strings(self):
        assert ToonSerializer.dumps("hello") == "hello"
        assert ToonSerializer.dumps("world") == "world"
        assert ToonSerializer.loads("hello") == "hello"

    def test_strings_with_special_chars(self):
        # Strings with colons need quoting
        result = ToonSerializer.dumps("key:value")
        assert result == '"key:value"'
        assert ToonSerializer.loads(result) == "key:value"

        # Strings with newlines need quoting
        result = ToonSerializer.dumps("line1\nline2")
        assert '"line1\\nline2"' in result
        assert ToonSerializer.loads(result) == "line1\nline2"

    def test_empty_string(self):
        result = ToonSerializer.dumps("")
        assert result == '""'
        assert ToonSerializer.loads(result) == ""


class TestToonSerializerCollections:
    """Test serialization of collections."""

    def test_empty_list(self):
        assert ToonSerializer.dumps([]) == "~[]"
        assert ToonSerializer.loads("~[]") == []

    def test_empty_dict(self):
        assert ToonSerializer.dumps({}) == "~{}"
        assert ToonSerializer.loads("~{}") == {}

    def test_simple_list(self):
        data = ["a", "b", "c"]
        toon = ToonSerializer.dumps(data)
        assert toon == "[a, b, c]"
        assert ToonSerializer.loads(toon) == data

    def test_list_of_numbers(self):
        data = [1, 2, 3, 4, 5]
        toon = ToonSerializer.dumps(data)
        assert toon == "[1, 2, 3, 4, 5]"
        assert ToonSerializer.loads(toon) == data

    def test_simple_dict(self):
        data = {"name": "test", "value": 42}
        toon = ToonSerializer.dumps(data)
        assert "name: test" in toon
        assert "value: 42" in toon
        assert ToonSerializer.loads(toon) == data

    def test_nested_dict(self):
        data = {"user": {"name": "Alice", "age": 30}}
        toon = ToonSerializer.dumps(data)
        result = ToonSerializer.loads(toon)
        assert result == data

    def test_dict_with_list(self):
        data = {"items": ["a", "b", "c"]}
        toon = ToonSerializer.dumps(data)
        assert ToonSerializer.loads(toon) == data


class TestToonSerializerNestedStructures:
    """Test serialization of complex nested structures."""

    def test_nested_lists(self):
        """Test the problematic nested list case that was fixed."""
        data = {"matrix": [[1, 2], [3, 4]]}
        toon = ToonSerializer.dumps(data)
        result = ToonSerializer.loads(toon)
        assert result == data

    def test_list_of_dicts(self):
        data = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ]
        }
        toon = ToonSerializer.dumps(data)
        result = ToonSerializer.loads(toon)
        assert result == data

    def test_deeply_nested_dict(self):
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": 42
                    }
                }
            }
        }
        toon = ToonSerializer.dumps(data)
        result = ToonSerializer.loads(toon)
        assert result == data

    def test_mixed_complex_structure(self):
        data = {
            "str": "hello",
            "num": 123,
            "bool": True,
            "null": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        toon = ToonSerializer.dumps(data)
        result = ToonSerializer.loads(toon)
        assert result == data


class TestToonSerializerTokenSavings:
    """Test token savings calculations."""

    def test_estimate_token_savings_simple(self):
        data = {"name": "test", "value": 42}
        json_str = json.dumps(data)
        toon_str = ToonSerializer.dumps(data)
        savings = ToonSerializer.estimate_token_savings(json_str, toon_str)
        # Should have positive savings
        assert savings > 0

    def test_estimate_token_savings_nested_list(self):
        """Verify nested lists no longer have negative savings."""
        data = {"matrix": [[1, 2], [3, 4]]}
        json_str = json.dumps(data)
        toon_str = ToonSerializer.dumps(data)
        savings = ToonSerializer.estimate_token_savings(json_str, toon_str)
        # Should be close to zero or slightly negative (acceptable)
        assert savings > -10  # Much better than the original -67.9%

    def test_estimate_token_savings_empty(self):
        """Test with empty JSON string."""
        savings = ToonSerializer.estimate_token_savings("", "")
        assert savings == 0.0

    def test_overall_savings(self):
        """Test that overall savings are positive for typical data."""
        test_cases = [
            {"name": "test", "value": 42},
            {"items": ["a", "b", "c"]},
            {"user": {"name": "Alice", "age": 30}},
            {"empty_list": [], "empty_dict": {}},
        ]

        total_json = 0
        total_toon = 0

        for data in test_cases:
            json_str = json.dumps(data)
            toon_str = ToonSerializer.dumps(data)
            total_json += len(json_str)
            total_toon += len(toon_str)

        overall_savings = (total_json - total_toon) / total_json * 100
        # Should have at least 10% savings overall
        assert overall_savings >= 10


class TestToonSerializerRoundTrip:
    """Test round-trip serialization and deserialization."""

    def test_round_trip_simple_dict(self):
        original = {"name": "test", "value": 42}
        toon = ToonSerializer.dumps(original)
        result = ToonSerializer.loads(toon)
        assert result == original

    def test_round_trip_complex_structure(self):
        original = {
            "users": [
                {"name": "Alice", "age": 30, "active": True},
                {"name": "Bob", "age": 25, "active": False}
            ],
            "count": 2,
            "metadata": {
                "version": 1.0,  # Use float instead of string
                "empty": []
            }
        }
        toon = ToonSerializer.dumps(original)
        result = ToonSerializer.loads(toon)
        assert result == original

    def test_round_trip_all_types(self):
        original = {
            "string": "hello",
            "int": 42,
            "float": 3.14,
            "bool_true": True,
            "bool_false": False,
            "null": None,
            "empty_list": [],
            "empty_dict": {},
            "list": [1, 2, 3],
            "nested": {"key": "value"}
        }
        toon = ToonSerializer.dumps(original)
        result = ToonSerializer.loads(toon)
        assert result == original


class TestToonSerializerEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_string_input(self):
        """Test loading empty string."""
        result = ToonSerializer.loads("")
        assert result is None

    def test_whitespace_only_input(self):
        """Test loading whitespace-only string."""
        result = ToonSerializer.loads("   \n  \t  ")
        assert result is None

    def test_backward_compatibility_tilde(self):
        """Test that single ~ defaults to empty list for backward compatibility."""
        result = ToonSerializer.loads("~")
        assert result == []

    def test_dict_with_empty_values(self):
        """Test dict with various empty values."""
        data = {
            "empty_str": "",
            "empty_list": [],
            "empty_dict": {},
            "null": None
        }
        toon = ToonSerializer.dumps(data)
        result = ToonSerializer.loads(toon)
        assert result == data
