from hashtable.hashtable_chaining import Node


def test_node_initialization():
    node = Node("test_key", "test_value")
    assert node.key == "test_key"
    assert node.value == "test_value"
    assert node.next is None


def test_node_representation():
    node = Node("test_key", "test_value")
    assert repr(node) == "test_key:test_value"


def test_node_linking():
    first_node = Node("first_key", "first_value")
    second_node = Node("second_key", "second_value")
    first_node.next = second_node
    assert first_node.next is second_node
    assert first_node.next.key == "second_key"
    assert first_node.next.value == "second_value"
    assert first_node.next.next is None
