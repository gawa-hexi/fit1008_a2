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

        print('= = '*20)
        print("\n\t@@@ LINEAR PROBE @@@\n")
        print("key1: ", key1)
        print("key2: ", key2)

        i1 = self.hash1(key1)
        print("index1: ", i1)


        # self.array[position1][1]key2] = data

        for i in range(len(self.array)):
            if self.array[i1] is None:
                break
            elif self.array[i1][0] == key1:
                break
            else:
                # print(self.array[i1][0])
                # print(key1)
                i1 = (i1 + 1) #% len(self.array)
                # print("new_index: ", i1)

        print("index1 (final): ", i1)


        if is_insert:
            sub_table = LinearProbeTable(self.internal_sizes)

            # if self.array[i1][1] is None:
                # self.array.__setitem__(i1, [key1, sub_table])
        else:
            sub_table = self.array[i1][1]
            # sub_sub_table = self.array[i1][1].

            # self.


            # self.array[position1][1][key2]
        if key2 is not None:
            try:

                # self.array[k2][1]
                # sub_table = self.array[i1][1]
                i2 = self.hash2(key2, sub_table)
                print("index2: ", i2)

                # if is_insert:
                    # sub_sub_table = LinearProbeTable()
                # else:
                    # sub_sub_table = sub_table.array[i2]

                probe_order = [i2, 4, 0, 1]
                start_i2 = i2
                # while True:
                #     if probe_order[0] != i2:
                #         probe_order.remove(probe_order[0])
                #     else:
                #         break

                    # i +=1
                # probe_order[i2] = probe_order
                # for i in probe_order:
                # self.array[position1][1].array[position2][1]

                    # break
                # sub_table.array[i1][1] =
                for i in probe_order: #range(len(sub_table.__len__())):
                    print("i: ", i2)
                    print("sub_table: ", sub_table.array[i2])
                    # print("sub_sub_table: ", sub_sub_table.array)

                    # if sub_table.array.__getitem__(i2) is None:
                        # sub_table.array.__setitem__(i2, [key2, None])

                    if sub_table.array[i2] is None:
                        if is_insert:
                            if not self.array[i1]:
                                # input(88)
                                self.array.__setitem__(i1, [key1, sub_table])
                            self.array[i1][1].array[i2] = (key2, None)
                            print("sub_table 232: ", type(sub_table.array[i2]))
                            return (i1, i2)
                        raise KeyError(f"Key2 '{key2}' not found")
                    # if sub_table.array[i2] is None:
                        # print("j")
                        print(sub_table.array[i2])
                        print("empty")
                        break

                    elif sub_table.array[i2][0] == key2:
                        print("match")
                        return (i1, i2)
                    # elif sub_table.array[i2] == key2:
                    #     print("keys match")
                    #     break
                    else:
                        print("increase")
                        i2 = i
                        print(i2)
                    if i2 == start_i2:
                        if is_insert:
                            raise FullError("Sub-table is full")  # Full table and no empty slot found
                        raise KeyError(f"Key2 '{key2}' not found")

            except KeyError:
                input()
            print("index2 (final): ", i2)


                # if is_insert:
                #     sub_table.__setitem__(key2, position2)
                # else:
                #     sub_table.__getitem__(key2)

        #
        #         print("/nPOS2: ", sub_table.array[position2])
        #         # position2 = sub_table._linear_probe(key2, is_insert)
        #         # sub_table[]
        #         print("\th2: ", position2)
        #     except KeyError:
        #         raise KeyError("Sub-key not found")
        #     return (position1, position2)
        # return position1


        # self.array[i1][i2]
        # sub_table.setitem(key2, )
        # self.array[i1] = (key1, sub_table)




        print(f"keys: ({i1}, {i2})")
        return i1, i2

        # raise NotImplementedError()

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

        key1, key2 = key
        position1, position2 = self._linear_probe(key1, key2, True)
        sub_table = self.array[position1][1]
        # print("sub_table: ", sub_table)
        if sub_table.is_empty():
            self.count += 1


        sub_table[key2] = data

        # resize if necessary
        if len(self) > self.table_size / 2:
            self._rehash()

        # print()

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


    class TestingDKT(DoubleKeyTable):
        def hash1(self, k):
            return ord(k[0]) % 12
        def hash2(self, k, sub_table):
            return ord(k[-1]) % 5

    dt = TestingDKT(sizes=[12], internal_sizes=[5])

    dt["Tim", "Jen"] = 1
    dt["Amy", "Ben"] = 2
    input("\n\n\n M1 \n\n")
    dt["May", "Ben"] = 3
    dt["Ivy", "Jen"] = 4
    input("\n\n\n M2 \n\n")
    dt["May", "Tom"] = 5
    dt["Tim", "Bob"] = 6

    # dt._linear_probe("May", "Tom", False)

    print()
    input("\n\n\n @@@@@@@@@@@@ \n\n")

    print(dt.__getitem__(["May", "Tom"]))
    dt._linear_probe("May", "Jim", True) #KeyError
    dt._linear_probe("May", "Jim", True) #(6, 1)

    print(dt.__getitem__(["May", "Tom"]))
    print(dt.__getitem__(["May", "Jim"]))
        # assertRaises(KeyError, l
    # assertEqual(dt._linear_probe("May", "Jim", True), (6, 1))


    # dt["May", "Jim"] = 7 # Linear probing on internal table
    # self.assertEqual(dt._linear_probe("May", "Jim", False), (6, 1))
    # self.assertRaises(KeyError, lambda: dt._linear_probe("Het", "Liz", False))
    # self.assertEqual(dt._linear_probe("Het", "Liz", True), (2, 2))
    # dt["Het", "Liz"] = 8 # Linear probing on external table
    # self.assertEqual(dt._linear_probe("Het", "Liz", False), (2, 2))
