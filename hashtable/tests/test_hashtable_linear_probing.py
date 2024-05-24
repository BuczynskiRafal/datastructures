import pytest

from hashtable.hashtable_linear_probing import HashTable


@pytest.fixture(scope="function")
def empty_ht():
    return HashTable(capacity=10)


@pytest.fixture(scope="function")
def filled_ht():
    ht = HashTable(capacity=10)
    for i in range(7):
        ht.insert(f"key{i}", f"value{i}")
    return ht


def test_insert_and_get(empty_ht):
    empty_ht.insert("key", "value")
    assert empty_ht.get("key") == "value"
    assert "key" in empty_ht
    assert len(empty_ht) == 1


def test_key_error_on_nonexistent_key(empty_ht):
    with pytest.raises(KeyError):
        empty_ht.get("nonexistent_key")


def test_update_existing_key(empty_ht):
    empty_ht.insert("key", "value1")
    empty_ht.insert("key", "value2")
    assert empty_ht.get("key") == "value2"


def test_remove_key(empty_ht):
    empty_ht.insert("key", "value")
    empty_ht.remove("key")
    assert "key" not in empty_ht
    with pytest.raises(KeyError):
        empty_ht.get("key")


def test_resize_functionality(filled_ht):
    initial_capacity = filled_ht.capacity
    filled_ht.insert("key_resize", "value_resize")
    assert filled_ht.capacity == 2 * initial_capacity
    assert filled_ht.get("key_resize") == "value_resize"
    for i in range(7):
        assert filled_ht.get(f"key{i}") == f"value{i}"


def test_rehash_on_remove(filled_ht):
    filled_ht.remove("key3")
    with pytest.raises(KeyError):
        filled_ht.get("key3")
    for i in range(7):
        if i != 3:
            assert filled_ht.get(f"key{i}") == f"value{i}"


def test_hash_collision_resolution(empty_ht):
    empty_ht.insert("key1", "value1")
    empty_ht.insert("key2", "value2")
    assert empty_ht.get("key1") == "value1"
    assert empty_ht.get("key2") == "value2"
