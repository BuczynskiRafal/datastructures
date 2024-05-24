class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * self.capacity

    def __str__(self):
        return str(
            [(i, entry) for i, entry in enumerate(self.table) if entry is not None]
        )

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.size

    def __contains__(self, key):
        try:
            _ = self.get(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def _hash(self, key, trial=0):
        c1, c2 = 1, 3
        return (hash(key) + c1 * trial + c2 * trial**2) % self.capacity

    def insert(self, key, value):
        if self.size / self.capacity >= 0.7:
            self.resize()

        trial = 0
        index = self._hash(key, trial)
        while self.table[index] is not None and self.table[index][0] != key:
            trial += 1
            index = self._hash(key, trial)

        if self.table[index] is None:
            self.size += 1
        self.table[index] = (key, value)

    def get(self, key):
        trial = 0
        index = self._hash(key, trial)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            trial += 1
            index = self._hash(key, trial)

        raise KeyError(f"There is no {key} in the collection.")

    def remove(self, key):
        trial = 0
        index = self._hash(key, trial)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = None
                self.size -= 1
                self._rehash_from(index)
                return
            trial += 1
            index = self._hash(key, trial)

        raise KeyError(f"There is no {key} in the collection.")

    def _rehash_from(self, start_index):
        next_index = (start_index + 1) % self.capacity
        while self.table[next_index] is not None:
            key, value = self.table[next_index]
            self.table[next_index] = None
            self.size -= 1
            self.insert(key, value)
            next_index = (next_index + 1) % self.capacity

    def resize(self):
        old_table = self.table
        old_capacity = self.capacity
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for index in range(old_capacity):
            if old_table[index] is not None:
                self.insert(*old_table[index])
