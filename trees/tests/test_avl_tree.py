import pytest
from trees.avl_tree import AVLTree, AVLNode


@pytest.fixture
def avl_tree():
    return AVLTree()


@pytest.fixture
def sample_tree(avl_tree):
    def _create_tree():
        root = None
        keys = [10, 20, 30, 40, 50, 25]
        for key in keys:
            root = avl_tree.insert(root, key)
        return root

    return _create_tree


def test_avl_node():
    node = AVLNode(10)
    assert node.key == 10
    assert node.left is None
    assert node.right is None
    assert node.height == 1


def test_get_height(avl_tree):
    node = AVLNode(10)
    assert avl_tree.get_height(None) == 0
    assert avl_tree.get_height(node) == 1


def test_get_balance(avl_tree):
    node = AVLNode(10)
    node.left = AVLNode(5)
    node.height = 2
    assert avl_tree.get_balance(node) == 1


@pytest.mark.parametrize(
    "rotation_func, setup_func, expected_root_key, expected_child_key",
    [
        (
            "rotate_right",
            lambda tree: AVLNode(30, AVLNode(20, None, AVLNode(25))),
            20,
            30,
        ),
        (
            "rotate_left",
            lambda tree: AVLNode(20, None, AVLNode(30, AVLNode(25))),
            30,
            20,
        ),
    ],
)
def test_rotations(
    avl_tree, rotation_func, setup_func, expected_root_key, expected_child_key
):
    root = setup_func(avl_tree)
    rotated = getattr(avl_tree, rotation_func)(root)
    assert rotated.key == expected_root_key
    assert (
        getattr(rotated, "right" if rotation_func == "rotate_right" else "left").key
        == expected_child_key
    )


def test_no_rotation_needed(avl_tree):
    root = None
    # Insert nodes in an order that keeps the tree balanced without rotations
    for key in [20, 10, 30, 5, 15, 25, 35]:
        root = avl_tree.insert(root, key)
    # Check the balance of each node to confirm no rotation was needed
    assert avl_tree.get_balance(root) in [-1, 0, 1]
    assert avl_tree.get_balance(root.left) in [-1, 0, 1]
    assert avl_tree.get_balance(root.right) in [-1, 0, 1]


def test_insert_and_balance(avl_tree):
    root = None
    for key in [10, 20, 30, 40, 50, 25]:
        root = avl_tree.insert(root, key)
    assert avl_tree.get_balance(root) in [-1, 0, 1]


@pytest.mark.parametrize(
    "key_to_delete, expected_traversal",
    [
        (10, [30, 20, 25, 40, 50]),
        (20, [30, 25, 10, 40, 50]),
        (30, [40, 20, 10, 25, 50]),
    ],
)
def test_delete_and_balance(
    avl_tree, sample_tree, key_to_delete, expected_traversal
):
    root = sample_tree()
    root = avl_tree.delete(root, key_to_delete)
    assert avl_tree.pre_order(root) == expected_traversal


def test_min_value_node(avl_tree, sample_tree):
    min_node = avl_tree.min_value_node(sample_tree())
    assert min_node.key == 10


def test_pre_order_traversal(avl_tree, sample_tree):
    assert avl_tree.pre_order(sample_tree()) == [30, 20, 10, 25, 40, 50]


def test_in_order_traversal(avl_tree, sample_tree):
    assert avl_tree.in_order(sample_tree()) == [10, 20, 25, 30, 40, 50]


def test_post_order_traversal(avl_tree, sample_tree):
    assert avl_tree.post_order(sample_tree()) == [10, 25, 20, 50, 40, 30]
