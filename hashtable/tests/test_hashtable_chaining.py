import pytest

from hashtable.hashtable_chaining import HashTable


@pytest.fixture(scope="function")
def empty_hash_table():
    return HashTable()


@pytest.fixture(scope="function")
def filled_hash_table():
    ht = HashTable()
    ht["key1"] = "value1"
    ht["key2"] = "value2"
    ht["key3"] = "value3"
    return ht


@pytest.fixture(scope="function")
def ht():
    return HashTable(capacity=10)


@pytest.fixture(scope="function")
def sample_ht():
    ht = HashTable(capacity=4)
    items = [
        ("key1", "value1"),
        ("key2", "value2"),
        ("key3", "value3"),
        ("key4", "value4"),
    ]
    for key, value in items:
        ht.insert(key, value)
    return ht


def test_hash_table_initialization(empty_hash_table):
    assert len(empty_hash_table) == 0
    assert empty_hash_table.capacity == 10


def test_hash_table_insert(empty_hash_table):
    empty_hash_table["key1"] = "value1"
    assert empty_hash_table["key1"] == "value1"
    assert len(empty_hash_table) == 1
    assert "key1" in empty_hash_table


def test_hash_table_update(empty_hash_table):
    empty_hash_table["key1"] = "value1"
    empty_hash_table["key1"] = "value2"
    assert empty_hash_table["key1"] == "value2"


def test_hash_table_remove(filled_hash_table):
    del filled_hash_table["key1"]
    with pytest.raises(KeyError):
        _ = filled_hash_table["key1"]


def test_hash_table_iter(filled_hash_table):
    assert sorted([key for key in filled_hash_table]) == sorted(
        ["key1", "key2", "key3"]
    )


def test_hash_table_contains(filled_hash_table):
    assert "key1" in filled_hash_table
    assert "key4" not in filled_hash_table


def test_hash_table_str_and_repr(filled_hash_table):
    expected = set(["key1:value1", "key2:value2", "key3:value3"])
    result = set(str(filled_hash_table)[1:-1].split(", "))
    assert result == expected


def test_hash_function(ht):
    key = "test_key"
    assert 0 <= ht._hash(key) < ht.capacity


def test_insert_new_key(ht):
    ht.insert("test_key", "test_value")
    assert ht.get("test_key") == "test_value"
    assert ht.size == 1


def test_update_existing_key(ht):
    ht.insert("test_key", "initial_value")
    ht.insert("test_key", "updated_value")
    assert ht.get("test_key") == "updated_value"
    assert ht.size == 1


def test_get_nonexistent_key(ht):
    with pytest.raises(KeyError):
        ht.get("nonexistent_key")


def test_hash_table_resize(ht):
    initial_capacity = ht.capacity
    for i in range(8):
        ht.insert(f"key{i}", f"value{i}")
    assert ht.capacity > initial_capacity
    for i in range(8):
        assert ht.get(f"key{i}") == f"value{i}"


def test_collision_handling(ht):
    keys = ["key1", "key2", "key3"]
    for key in keys:
        ht.insert(key, f"value_for_{key}")
    for key in keys:
        assert ht.get(key) == f"value_for_{key}"


def test_remove_existing_key(sample_ht):
    sample_ht["key2"] = "value2"

    assert "key2" in sample_ht
    assert len(sample_ht) == 11

    sample_ht.remove("key2")
    assert "key2" not in sample_ht
    assert len(sample_ht) == 10


def test_remove_nonexistent_key_raises_error(sample_ht):
    with pytest.raises(KeyError):
        sample_ht.remove("nonexistent_key")


def test_resize_doubles_capacity(sample_ht):
    original_capacity = sample_ht.capacity
    sample_ht.resize()
    assert sample_ht.capacity == 2 * original_capacity
    assert "key1" in sample_ht
    assert "key2" in sample_ht
    assert "key3" in sample_ht
    assert "key4" in sample_ht


def test_resize_maintains_data_integrity(sample_ht):
    original_items = {key: sample_ht.get(key) for key in sample_ht}
    sample_ht.resize()
    resized_items = {key: sample_ht.get(key) for key in sample_ht}
    assert original_items == resized_items
