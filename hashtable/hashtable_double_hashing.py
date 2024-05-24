class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * self.capacity

    def __str__(self):
        return str([entry for entry in self.table if entry is not None])

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.size

    def __contains__(self, key):
        index, _ = self._find_slot(key, for_insert=False)
        return index is not None

    def __getitem__(self, key):
        index, _ = self._find_slot(key, for_insert=False)
        if index is None:
            raise KeyError(f"There is no {key} in the collection.")
        return self.table[index][1]

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def _hash1(self, key):
        return hash(key) % self.capacity

    def _hash2(self, key):
        return 1 + (hash(key) % (self.capacity - 1))

    def _find_slot(self, key, for_insert):
        index = self._hash1(key)
        step = self._hash2(key)

        first_index = None
        while True:
            if self.table[index] is None:
                if not for_insert:
                    return None, None
                return index if first_index is None else first_index, step

            elif self.table[index][0] == key:
                return index, step

            elif first_index is None and self.table[index] is False:
                first_index = index

            index = (index + step) % self.capacity

    def insert(self, key, value):
        if self.size / self.capacity >= 0.7:
            self.resize()

        index, step = self._find_slot(key, for_insert=True)
        if index is not None:
            self.table[index] = (key, value)
            self.size += 1

    def get(self, key):
        index, _ = self._find_slot(key, for_insert=False)
        if index is None:
            raise KeyError(f"There is no {key} in the collection.")
        return self.table[index][1]

    def remove(self, key):
        index, step = self._find_slot(key, for_insert=False)
        if index is None:
            raise KeyError(f"There is no {key} in the collection.")
        self.table[index] = None
        self.size -= 1

        next_index = (index + step) % self.capacity
        while self.table[next_index] is not None:
            key_to_rehash, value_to_rehash = self.table[next_index]
            self.table[next_index] = None
            self.size -= 1
            self.insert(key_to_rehash, value_to_rehash)
            next_index = (next_index + step) % self.capacity

    def resize(self):
        old_table = self.table
        old_capacity = self.capacity
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for index in range(old_capacity):
            if old_table[index] is not None:
                self.insert(*old_table[index])
