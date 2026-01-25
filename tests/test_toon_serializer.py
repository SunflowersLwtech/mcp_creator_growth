from mcp_creator_growth.storage.toon_serializer import serialize_to_toon

def test_serialize_simple_dict():
    data = {"name": "test", "value": 123}
    expected = "name: test\nvalue: 123"
    assert serialize_to_toon(data) == expected

def test_serialize_nested_dict():
    data = {"user": {"id": 1, "active": True}}
    expected = "user:\n  id: 1\n  active: true"
    assert serialize_to_toon(data) == expected

def test_serialize_list():
    data = ["item1", "item2"]
    expected = "- item1\n- item2"
    assert serialize_to_toon(data) == expected

def test_serialize_complex_list():
    data = [{"id": 1}, {"id": 2}]
    # Based on simplified implementation:
    # -
    #   id: 1
    # -
    #   id: 2
    expected = "-\n  id: 1\n-\n  id: 2"
    assert serialize_to_toon(data) == expected
