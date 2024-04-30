from __future__ import annotations
from computer import Computer
from algorithms import binary_search

class ComputerOrganiser:
    def __init__(self):
        self.computers = []

    def add_computers(self, new_computers):
        for computer in new_computers:
            # Find insertion point using custom binary search
            index = binary_search.binary_search(self.computers,computer)
            # Insert into the sorted list at the correct position
            self.computers.insert(index, computer)

    def cur_position(self, computer):
        try:
            index = self.computers.index(computer)
            return index
        except ValueError:
            raise KeyError("Computer not found in the list.")