from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes

        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES

        self.size_index = 0
        self.array: ArrayR[tuple[K1, V] | None] | None = ArrayR(self.TABLE_SIZES[self.size_index])
        #print("Initializing array with size:", self.TABLE_SIZES[self.size_index])
        self.count = 0


    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        """
        hash1 = ord(key[0]) % self.table_size

        return hash1

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        """

        hash2 = ord(key[-1]) % sub_table.table_size

        return hash2

    def _linear_probe(self, key1: K1, key2: K2 | None, is_insert: bool) -> tuple[int, int] | int:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        # Calculate hash1 and initial position
        hash1 = self.hash1(key1)
        position1 = hash1 % self.table_size

        # print(f"Hash1 for key1 '{key1}': {hash1}")
        # print(f"Initial position1: {position1}")

        # Linear probing for the top-level table
        while self.array[position1] is not None and self.array[position1][0] != key1:
            # print(f"Collision at position1 {position1} for key1 '{key1}'. Probing to the next position.")
            position1 = (position1 + 1) % self.table_size

        if self.array[position1] is None:
            if is_insert:
                # print(f"Inserting new key1 '{key1}' at position {position1}. Creating internal table.")
                # Create a new internal hash table
                internal_table = LinearProbeTable(self.internal_sizes)
                internal_table.hash = lambda k, tab=internal_table: self.hash2(k, tab)
                self.array[position1] = (key1, internal_table)
            else:
                # print(f"Key1 '{key1}' not found. Raising KeyError.")
                raise KeyError("Key not found in the top-level table.")

        if key2 is None:
            # print(f"Returning top-level position: {position1}")
            return position1  # Return only the top-level position

        # Get the internal table and compute its hash
        sub_table = self.array[position1][1]
        hash2 = self.hash2(key2, sub_table)
        position2 = hash2 % sub_table.table_size

        # print(f"Hash2 for key2 '{key2}': {hash2}")
        # print(f"Initial position2 in sub-table: {position2}")

        # Linear probing for the internal table
        while sub_table.array[position2] is not None and sub_table.array[position2][0] != key2:
            # print(f"Collision at position2 {position2} for key2 '{key2}'. Probing to the next position.")
            position2 = (position2 + 1) % sub_table.table_size

        if sub_table.array[position2] is None:
            if not is_insert:
                raise KeyError("Key not found in the internal table.")

        # print(f"Returning positions: {position1}, {position2}")
        return position1, position2  # Return both top and sub-level positions


    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            # Iterate through the top-level table
            for element in self.array:
                if element is not None:
                    yield element[0]
        else:
            # Find the position for the top-level key and iterate through its sub-table
            position1 = self._linear_probe(key, None, False)
            sub_table = self.array[position1][1]
            for element in sub_table.array:
                if element is not None:
                    yield element[0]

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        if key is None:
            # Iterate through the top-level table and yield all values from the sub-tables
            for element in self.array:
                if element is not None:
                    sub_table = element[1]
                    for sub_element in sub_table.array:
                        if sub_element is not None:
                            yield sub_element[1]
        else:
            # Find the position for the top-level key and yield all values from its sub-table
            position1 = self._linear_probe(key, None, False)
            sub_table = self.array[position1][1]
            for sub_element in sub_table.array:
                if sub_element is not None:
                    yield sub_element[1]

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        if key is None:
            # Get all top-level keys
            return list(self.iter_keys())
        else:
            # Get all sub-level keys for the specified top-level key
            return list(self.iter_keys(key))


    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        if key is None:
            # Get all values in the entire double key table
            return list(self.iter_values())
        else:
            # Get all values in the sub-table for the specified top-level key
            return list(self.iter_values(key))

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

        position1, position2 = self._linear_probe(key[0], key[1], False)
        return self.array[position1][1].array[position2][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        position1, position2 = self._linear_probe(key[0], key[1], True)
        sub_table = self.array[position1][1]

        if sub_table.is_empty():
            self.count += 1

        sub_table[key[1]] = data

        # resize if necessary
        if len(self) >= self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        position1, position2 = self._linear_probe(key[0], key[1], False)
        sub_table = self.array[position1][1]
        if sub_table.array[position2] is None:
            raise KeyError("Key not found for deletion.")

        # Remove the item and update the count
        sub_table.array[position2] = None

        if all(x is None for x in sub_table.array):
            # If the internal table becomes empty, clear it
            self.array[position1] = None
            self.count -= 1

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """

        old_array = self.array

        self.size_index += 1

        if self.size_index >= len(self.TABLE_SIZES):
            new_table_size = self.TABLE_SIZES[-1] + 1
            self.TABLE_SIZES.append(new_table_size)

        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

        for element in old_array:
            if element is not None:
                key1, sub_table = element
                position1 = self.hash1(key1)
                for element2 in sub_table.array:
                    if element2 is not None:
                        key2, value = element2
                        self[key1,key2] = value

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
    print("string test")
