class NaryNode:
    def __init__(self, key):
        self.val = key
        self.children = []


class NaryTree:
    def __init__(self, n):
        self.root = None
        self.n = n

    def insert(self, key):
        new_node = NaryNode(key)
        if not self.root:
            self.root = new_node
        else:
            queue = [self.root]
            while queue:
                node = queue.pop(0)
                if len(node.children) < self.n:
                    node.children.append(new_node)
                    return
                else:
                    queue.extend(node.children)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if not node:
            return None
        if node.val == key:
            return node
        for child in node.children:
            result = self._search_recursive(child, key)
            if result:
                return result
        return None

    def delete(self, key):
        if not self.root:
            return False
        if self.root.val == key:
            self.root = None
            return True
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            for i, child in enumerate(node.children):
                if child.val == key:
                    node.children.pop(i)
                    return True
                else:
                    queue.append(child)
        return False

    def height(self):
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if not node:
            return 0
        if not node.children:
            return 1
        heights = [self._height_recursive(child) for child in node.children]
        return max(heights) + 1

    def count_nodes(self):
        return self._count_nodes_recursive(self.root)

    def _count_nodes_recursive(self, node):
        if not node:
            return 0
        count = 1
        for child in node.children:
            count += self._count_nodes_recursive(child)
        return count

    def is_balanced(self):
        return self._is_balanced_recursive(self.root)

    def _is_balanced_recursive(self, node):
        if not node:
            return True
        child_heights = [self._height_recursive(child) for child in node.children]
        if max(child_heights, default=0) - min(child_heights, default=0) > 1:
            return False
        for child in node.children:
            if not self._is_balanced_recursive(child):
                return False
        return True

    def preorder_traversal(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if not node:
            return
        result.append(node.val)
        for child in node.children:
            self._preorder_recursive(child, result)

    def postorder_traversal(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if not node:
            return
        for child in node.children:
            self._postorder_recursive(child, result)
        result.append(node.val)

    def bfs_traversal(self):
        if not self.root:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.val)
            queue.extend(node.children)
        return result


# Przykładowe użycie
nt = NaryTree(3)  # Tworzymy drzewo ternarne (3-ary)
nt.insert(1)
nt.insert(2)
nt.insert(3)
nt.insert(4)
nt.insert(5)
nt.insert(6)
nt.insert(7)

# Wyświetlenie elementów drzewa
print("Preorder Traversal of the n-ary tree:")
print(nt.preorder_traversal())
print("Postorder Traversal of the n-ary tree:")
print(nt.postorder_traversal())
print("BFS Traversal of the n-ary tree:")
print(nt.bfs_traversal())

# Dodatkowe funkcjonalności
print("Height of the n-ary tree:", nt.height())
print("Total number of nodes in the n-ary tree:", nt.count_nodes())
print("Is the n-ary tree balanced?", nt.is_balanced())

# Wyszukiwanie i usuwanie
search_key = 5
found_node = nt.search(search_key)
print(f"Node with value {search_key} found:", found_node is not None)

delete_key = 3
nt.delete(delete_key)
print(f"Preorder traversal after deleting {delete_key}:")
print(nt.preorder_traversal())
