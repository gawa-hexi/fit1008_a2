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
        self.count = 0



    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2 | None, is_insert: bool) -> tuple[int, int] | int:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        # raise NotImplementedError()
            # Get the index for the top-level table

        print("\nk1: ", key1)
        print("k2: ", key2)
        print("hash1: ", self.hash1(key1))
        print("length: ", self.array.__len__())
        position1 = self.hash1(key1) % len(self.array)
        print(position1)
        sub_table = self.array[position1]
        print("sub_table: ", sub_table)

        # print("3231: ", self.array[position1].__getitem__(position1))
        print("pos1: ", self.array[position1])
        print(type(self.array[position1]))
        # try:
            # print("pos1: ", self.array[position1][0])
        # except:
            # pass
        for _ in range(len(self.array)):
            if self.array[position1] is None:
                break
                # Empty spot. Am I upserting or retrieving?
                # if is_insert:
                    # return position
                # else:
                    # raise KeyError(key)
            elif self.array[position1][1] == key1:
                break
            else:
                position1 = (position1 + 1) % len(self.array)

        # while (self.array[position1] is not None) and (self.array[position1][0] != key1): #!= (key1 or None):
        # # while self.array[position1] is not None and self.array[position1][0]:
        #     position1 += 1
        #     # sub_table = self.array[position1]
        #     print("new pos: ", self.array[position1], "\nindex: ", position1)
        #     # p
        # if sub_table is not None:
            # posit
        input(32321)

        print('@@@@@@@@2')
        if is_insert:
            sub_table = LinearProbeTable(self.internal_sizes)
            self.array[position1] = sub_table
        else:
            raise KeyError("Key not found")
    # else:

        print("\n\n\th1: ",position1)



        if key2 is not None:
            try:
                # print(position2)
                position2 = self.hash2(key2, sub_table) #% len(sub_table.array)
                print("pos2: ", position2)

                probe_order = [4, 0, 1]
                while sub_table.array[position2] is not None:
                    # position2
                    position2 += 1
                    print("new pos: ", self.array[position1], "\nindex: ", position1)



                if is_insert:
                    sub_table.__setitem__(key2, position2)
                else:
                    sub_table.__getitem__(key2)
            # else:
                # position2 = self.hash2(key2, sub_table
                # )
                # sub_table.array[position2]
                # position2_copy = position2
                # while sub_table.array[position2] is not None and sub_table.array[position2] != key2:
                    # position2 = (position2 + 1) #% len(sub_table.array)

                    # if position2 == position2_copy:
                        # raise FullError("Sub-table is full")

                # sub_table.array[position2]

                print("/nPOS2: ", sub_table.array[position2])
                # position2 = sub_table._linear_probe(key2, is_insert)
                # sub_table[]
                print("\th2: ", position2)
            except KeyError:
                raise KeyError("Sub-key not found")
            return (position1, position2)
        return position1



        if key2 is not None:
            try:
                # print(position2)
                position2 = sub_table._linear_probe(key2, is_insert)
                print("\th2: ", position2)
            except KeyError:
                raise KeyError("Sub-key not found")
            return (position1, position2)
        return position1

        #
        #  if key2 is not None:
        # index2 = sub_table.hash(key2)   # Make sure to use the sub-table's hash method
        # if not is_insert:
        #     # For retrieval, simply return the calculated indices if the key exists
        #     if sub_table.array[index2] is None or sub_table.array[index2][0] != key2:
        #         raise KeyError(f"Key {key2} not found in sub-table of {key1}")
        # else:
        #     # For insertion, find the next empty slot using linear probing
        #     original_index2 = index2
        #
        # return (index1, index2)





    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        raise NotImplementedError()

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        raise NotImplementedError()

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


        print("data: ", data)
        print("key: ", key)



        key1, key2 = key
        # print("key1: ", key1)
        # print("key2: ", key2)
        # print(self)
        position1, position2 = self._linear_probe(key1, key2, True)
        sub_table = self.array[position1]
        # print(type(sub_table))
        self.array[position1].array[position2] = (key2, data)
        # print(self.array[position1].array[position2])
        # input()
    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        raise NotImplementedError()

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
        raise NotImplementedError()
if __name__=="__main__":


        # Disable resizing / rehashing.
        class TestingDKT(DoubleKeyTable):
            def hash1(self, k):
                # input()
                print(ord(k[0]))
                return ord(k[0]) % 12
            def hash2(self, k, sub_table):
                return ord(k[-1]) % 5

        dt = TestingDKT(sizes=[12], internal_sizes=[5])

        # dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        # dt["May", "Ben"] = 3
        # dt["Ivy", "Jen"] = 4
        # dt["May", "Tom"] = 5
        # dt["Tim", "Bob"] = 6
        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["May", "Ben"] = 3
        dt["Ivy", "Jen"] = 4
        dt["May", "Tom"] = 5
        dt["Tim", "Bob"] = 6
        print("get response:")
        # x = dt._linear_probe("Tim", "Bob", False)
        x = dt._linear_probe("May", "Jim", True)
        print(x)

        #
        # self.assertRaises(KeyError, lambda: dt._linear_probe("May", "Jim", False))
        # self.assertEqual(dt._linear_probe("May", "Jim", True), (6, 1))
        # dt["May", "Jim"] = 7 # Linear probing on internal table
        # self.assertEqual(dt._linear_probe("May", "Jim", False), (6, 1))
        # self.assertRaises(KeyError, )

        # lambda: dt._linear_probe("Het", "Liz", False)
        # print("\n\n     @@@@@@   @@@@@   @@@@@@")
        # dt._linear_probe("Het", "Liz", False)

        # self.assertEqual(dt._linear_probe("Het", "Liz", True), (2, 2))
        # dt["Het", "Liz"] = 8 # Linear probing on external table
        # self.assertEqual(dt._linear_probe("Het", "Liz", False), (2, 2))
