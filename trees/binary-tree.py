class Node:
    def __init__(self, key) -> None:
        self.right = None
        self.left = None
        self.val = key


class BinaryTree:
    def __init__(self) -> None:
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.val:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_recursive(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursive(node.right, key)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.val == key:
            return node
        if key < node.val:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        if not node:
            return node

        if key < node.val:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.val:
            node.right = self._delete_recursive(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self._min_value_node(node.right)
            node.val = temp.val
            node.right = self._delete_recursive(node.right, temp.val)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def height(self):
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if not node:
            return 0
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        return max(left_height, right_height) + 1

    def count_nodes(self):
        return self._count_nodes_recursive(self.root)

    def _count_nodes_recursive(self, node):
        if not node:
            return 0
        return (
            1
            + self._count_nodes_recursive(node.left)
            + self._count_nodes_recursive(node.right)
        )

    def is_balanced(self):
        return self._is_balanced_recursive(self.root)

    def _is_balanced_recursive(self, node):
        if not node:
            return True
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        if abs(left_height - right_height) > 1:
            return False
        return self._is_balanced_recursive(node.left) and self._is_balanced_recursive(
            node.right
        )

    def inorder_traversal(self):
        return self._inorder_traversal(self.root)

    def _inorder_traversal(self, node):
        result = []
        if node:
            result = self._inorder_traversal(node.left)
            result.append(node.val)
            result += self._inorder_traversal(node.right)
        return result

    def preorder_traversal(self):
        return self._preorder_traversal(self.root)

    def _preorder_traversal(self, node):
        result = []
        if node:
            result.append(node.val)
            result += self._preorder_traversal(node.left)
            result += self._preorder_traversal(node.right)
        return result

    def postorder_traversal(self):
        return self._postorder_traversal(self.root)

    def _postorder_traversal(self, node):
        result = []
        if node:
            result = self._postorder_traversal(node.left)
            result += self._postorder_traversal(node.right)
            result.append(node.val)
        return result

    def bfs_traversal(self):
        if not self.root:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result


bt = BinaryTree()
bt.insert(50)
bt.insert(30)
bt.insert(20)
bt.insert(40)
bt.insert(70)
bt.insert(60)
bt.insert(80)

# Displaying elements of the tree
print("Inorder Traversal of the binary tree:")
print(bt.inorder_traversal())
print("Preorder Traversal of the binary tree:")
print(bt.preorder_traversal())
print("Postorder Traversal of the binary tree:")
print(bt.postorder_traversal())
print("BFS Traversal of the binary tree:")
print(bt.bfs_traversal())

# Additional functionalities
print("Height of the binary tree:", bt.height())
print("Total number of nodes in the binary tree:", bt.count_nodes())
print("Is the binary tree balanced?", bt.is_balanced())

# Searching and Deleting
search_key = 40
found_node = bt.search(search_key)
print(f"Node with value {search_key} found:", found_node is not None)

delete_key = 70
bt.delete(delete_key)
print(f"Inorder traversal after deleting {delete_key}:")
print(bt.inorder_traversal())
