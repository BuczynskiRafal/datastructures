import pytest

from hashtable.hashtable_double_hashing import HashTable


@pytest.fixture(scope="function")
def empty_ht():
    return HashTable(capacity=10)


@pytest.fixture(scope="function")
def filled_ht():
    ht = HashTable(capacity=10)
    for num in range(6):
        ht.insert(f"key{num}", f"value{num}")
    return ht


def test_insert_and_get(empty_ht):
    empty_ht.insert("key1", "value1")
    assert empty_ht.get("key1") == "value1"
    assert "key1" in empty_ht
    assert len(empty_ht) == 1


def test_key_error_on_nonexistent_key(empty_ht):
    with pytest.raises(KeyError):
        empty_ht.get("nonexistent_key")


def test_collision_handling_and_double_hashing(empty_ht):
    empty_ht.insert("key1", "value1")
    empty_ht.insert("key2", "value2")
    assert empty_ht.get("key1") == "value1"
    assert empty_ht.get("key2") == "value2"


def test_update_value(empty_ht):
    empty_ht.insert("key1", "value1")
    empty_ht.insert("key1", "updated_value")
    assert empty_ht.get("key1") == "updated_value"


def test_remove_key(filled_ht):
    assert filled_ht
    filled_ht.remove("key4")
    assert "key4" not in filled_ht
    with pytest.raises(KeyError):
        filled_ht.get("key4")


def test_rehash_after_removal(filled_ht):
    if "key4" not in filled_ht:
        filled_ht.insert("key4", "value4")
    filled_ht.remove("key4")
    for num in range(5):
        if num != 4:
            assert filled_ht.get(f"key{num}") == f"value{num}"


def test_resize(empty_ht):
    for num in range(7):
        empty_ht.insert(f"key{num}", f"value{num}")
    assert empty_ht.capacity == 10
    empty_ht.insert("key7", "value7")
    assert empty_ht.capacity == 20
    for num in range(7):
        assert empty_ht.get(f"key{num}") == f"value{num}"


def test_hash_table_len_and_contains(filled_ht):
    assert len(filled_ht) == 6
    assert "key1" in filled_ht
    assert "key999" not in filled_ht


def test_hash_table_str_and_repr(filled_ht):
    expected_keys = [f"key{i}" for i in range(6)]
    result_keys = [entry[0] for entry in filled_ht.table if entry is not None]
    assert sorted(expected_keys) == sorted(result_keys)


def test_clear_and_empty(empty_ht):
    empty_ht.insert("key1", "value1")
    empty_ht.remove("key1")
    assert len(empty_ht) == 0
    assert "key1" not in empty_ht
