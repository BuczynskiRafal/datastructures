class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __repr__(self) -> str:
        return f"{self.key}:{self.value}"


class HashTable:
    def __init__(self, capacity=10) -> None:
        self.size = 0
        self.capacity = capacity
        self.table = [None] * self.capacity

    def __str__(self):
        return str([node for node in self.table if node is not None])

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self):
        return self.size

    def __iter__(self):
        for slot in self.table:
            current = slot
            while current:
                yield current.key
                current = current.next

    def __contains__(self, key):
        try:
            return self.get(key) is not None
        except KeyError:
            return False

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        if self.size / self.capacity >= 0.7:
            self.resize()

        index = self._hash(key)
        current = self.table[index]
        if current is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = Node(key, value)
            self.size += 1

    def get(self, key):
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"There is no {key} in the collection.")

    def remove(self, key):
        index = self._hash(key)
        previous, current = None, self.table[index]
        while current:
            if current.key == key:
                if previous is None:
                    self.table[index] = current.next
                else:
                    previous.next = current.next
                self.size -= 1
                return
            previous, current = current, current.next
        raise KeyError(f"There is no {key} in the collection.")

    def resize(self):
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        for slot in old_table:
            current = slot
            while current:
                self.insert(current.key, current.value)
                current = current.next
