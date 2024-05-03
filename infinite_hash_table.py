from __future__ import annotations
from typing import Generic, TypeVar
from algorithms import mergesort

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        self.array: ArrayR[tuple[K, V] | None] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = level
    
    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        index = self.hash(key)

        if self.array[index] is None:
            raise KeyError(f"Key '{key}' not found")
        elif isinstance(self.array[index], tuple):
            if self.array[index][0] == key:
                return self.array[index][1]
            else:
                raise KeyError(f"Key '{key}' not found")
        else:
            return self.array[index][key]


    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        index = self.hash(key)

        if self.array[index] is None:
            self.array[index] = (key, value)
            self.count += 1
            
        elif isinstance(self.array[index], tuple):
            if self.array[index][0] == key:
                self.array[index] = (key, value)
                
            else:
                new_array = InfiniteHashTable(self.level + 1)
                newKey, newValue = self.array[index]
                new_array[newKey] = newValue
                new_array[key] = value
                self.array[index] = new_array
                self.count += 1
                
        else:
            self.array[index][key] = value
            self.count += 1


    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        index = self.hash(key)

        if self.array[index] is None:
            raise KeyError(f"Key '{key}' not found")
        elif isinstance(self.array[index], tuple):
            if self.array[index][0] == key:
                self.array[index] = None  
                self.count -= 1
            else:
                raise KeyError(f"Key '{key}' not found")
        else:
            sub_table = self.array[index]
            if not isinstance(sub_table, InfiniteHashTable):
                raise KeyError(f"Expected InfiniteHashTable but found different type")

            del sub_table[key]
            
            def count_active_entries(sub_table):
                active = []
                for item in sub_table.array:
                    if item is None:
                        continue
                    if isinstance(item, tuple):
                        active.append(item)  # Direct key-value pair
                    elif isinstance(item, InfiniteHashTable):
                        active.extend(count_active_entries(item))  # Recursively count sub-tables
                return active
            
            active = count_active_entries(sub_table)

            if len(active) == 1:
                self.array[index] = active[0]
                self.count -= 1

    def __len__(self) -> int:
        counter = 0

        def count_entries(current):
            for item in current.array:
                nonlocal counter
                if item is None:
                    continue
                if isinstance(item, tuple):
                    counter += 1  # Count active key-value pairs
                elif isinstance(item, InfiniteHashTable):
                    count_entries(item)  # Recursively count sub-tables

        count_entries(self)  # Start counting from the top-level hash table
        return counter
    
    
    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        keyLocation = []
        cur = self

        while True:
            index = cur.hash(key)
            keyLocation.append(index)

            if isinstance(cur.array[index], InfiniteHashTable):
                cur = cur.array[index]  
            elif isinstance(cur.array[index], tuple):
                if cur.array[index][0] == key:
                    break
                else:
                    raise KeyError(f"Key '{key}' not found")
            else:
                raise KeyError(f"Key '{key}' not found")
        return keyLocation

    def __contains__(self, key: K) -> bool:
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

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        """
        keys = []
        def traverse(current):
            for i in current.array:
                if i is None:
                    continue
                if isinstance(i, tuple):
                    keys.append(i[0])
                elif isinstance(i, InfiniteHashTable):
                    traverse(i)  
        traverse(self)
        return mergesort.mergesort(keys) 
