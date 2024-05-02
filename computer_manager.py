from __future__ import annotations
from computer import Computer
from algorithms import mergesort


class ComputerManager:

    def __init__(self) -> None:
        self.computers = []

    def add_computer(self, computer: Computer) -> None:
        if computer not in self.computers:
            self.computers.append(computer)

    def remove_computer(self, computer: Computer) -> None:
        if computer in self.computers:
            self.computers.remove(computer)


    def edit_computer(self, old: Computer, new: Computer) -> None:
        if old in self.computers:
            index = self.computers.index(old)
            self.computers[index] = new


    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        return [comp for comp in self.computers if getattr(comp, 'hacking_difficulty', None) == diff]

    def group_by_difficulty(self) -> list[list[Computer]]:
        grouped = {}
        for comp in self.computers:
            diff = getattr(comp, 'hacking_difficulty', None)
            if diff not in grouped:
                grouped[diff] = []
            grouped[diff].append(comp)

        #mergesort has complexity O(nlogn)
        sorted_difficulties = mergesort.mergesort(list(grouped.keys()))

        return [grouped[difficulty] for difficulty in sorted_difficulties]
