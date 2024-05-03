from __future__ import annotations
from computer import Computer
from algorithms import binary_search

def computer_sort_key(computer: Computer):
        return (computer.hacking_difficulty, computer.risk_factor, computer.name)

class ComputerOrganiser:
    def __init__(self):
        self.computers = []

    def add_computers(self, computers: list[Computer]) -> None:
        for computer in computers:
            index = binary_search.binary_search(self.computers, computer)
            self.computers.insert(index, computer)
    
    def _find_insertion_point(self, computer: Computer) -> int:
       
        return binary_search.binary_search(
            self.computers, computer, key=computer_sort_key
        )

    def cur_position(self, computer):
        try:
            index = self.computers.index(computer)
            return index
        except ValueError:
            raise KeyError("Computer not found in the list.")