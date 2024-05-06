from __future__ import annotations
from computer import Computer
from algorithms import binary_search

def computer_sort_key(computer: Computer):
        return (computer.hacking_difficulty, computer.risk_factor, computer.name)

class ComputerOrganiser:
    def __init__(self):
        """
        Initializes the ComputerOrganiser with an empty list

        COMPLEXITY:
            O(n): best & worst case = O(1)
        """
        self.computers = []

    def add_computers(self, computers: list[Computer]) -> None:
        """
        Adds list of computers to the sorted list.
        Each computer is put into the correct position. This is decided by the binary search

        COMPLEXITY:
            O(n): best case = O(m log n);
            O(n): worst case = O(mn)
            where m is the no. of computers being added,
            and n is the no. of computers already in the list
        """
        for computer in computers:
            index = binary_search.binary_search(self.computers, computer)
            self.computers.insert(index, computer)

    def _find_insertion_point(self, computer: Computer) -> int:
        """
        Finds the node to insert at via binary search

        COMPLEXITY:
            O(n): best case = O(log n);
             O(n): worst case = O(log n),
             where n is the no. of computers in the list
        """

        return binary_search.binary_search(
            self.computers, computer, key=computer_sort_key
        )

    def cur_position(self, computer):
        """
        Returns the current index of the computer in the list;
        raises an error if the computer is not found.

        COMPLEXITY:
            O(n): best case = O(1);
            O(n): worst case = O(n) (comp = last element // present),
            where n is the no. of computers in the list

        """
        try:
            index = self.computers.index(computer)
            return index
        except ValueError:
            raise KeyError("Computer not found in the list.")
