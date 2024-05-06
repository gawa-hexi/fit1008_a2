from __future__ import annotations
from computer import Computer
from algorithms import mergesort


class ComputerManager:

    def __init__(self) -> None:
        """
        COMPLEXITY:
        O(n): best case & worst case = O(1)

        """
        self.computers = []

    def add_computer(self, computer: Computer) -> None:
        """
        Adds computer to the computers list (if not already included)

        COMPLEXITY:
            O(n): best case = O(1);
            O(n): worst case = O(n), where n is the number of computers.
        """
        if computer not in self.computers:
            self.computers.append(computer)

    def remove_computer(self, computer: Computer) -> None:
        """
        COMPLEXITY:
            O(n): best case = O(1);
            O(n): worst case = O(n), where n is the number of computers
        """
        if computer in self.computers:
            self.computers.remove(computer)


    def edit_computer(self, old: Computer, new: Computer) -> None:
        """
        COMPLEXITY:
            O(n): best case = O(1);
            O(n): worst case = O(n), where n is the number of computers
        """
        if old in self.computers:
            index = self.computers.index(old)
            self.computers[index] = new


    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        """
        COMPLEXITY:
            O(n): best case = O(1);
            O(n): worst case = O(n), where n is the number of computers
        """
        return [comp for comp in self.computers if getattr(comp, 'hacking_difficulty', None) == diff]

    def group_by_difficulty(self) -> list[list[Computer]]:
        """
        COMPLEXITY:
            O(n): best case = O(n);
            O(n): worst case = O(n + log b), 
                with n being number of computers,
                and b being the number of difficulty levels
        """
        grouped = {}
        for comp in self.computers:
            diff = getattr(comp, 'hacking_difficulty', None)
            if diff not in grouped:
                grouped[diff] = []
            grouped[diff].append(comp)

        #mergesort has complexity O(nlogn)
        sorted_difficulties = mergesort.mergesort(list(grouped.keys()))

        return [grouped[difficulty] for difficulty in sorted_difficulties]
