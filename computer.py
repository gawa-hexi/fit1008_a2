from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Computer:

    name: str
    hacking_difficulty: int
    hacked_value: int
    risk_factor: float

    def __lt__(self, other):
        if not isinstance(other, Computer):
            return NotImplemented
        if self.hacking_difficulty != other.hacking_difficulty:
            return self.hacking_difficulty < other.hacking_difficulty
        if self.risk_factor != other.risk_factor:
            return self.risk_factor < other.risk_factor
        return self.name < other.name 

    def __eq__(self, other):
        if not isinstance(other, Computer):
            return NotImplemented
        return (
            self.name == other.name and 
            self.hacking_difficulty == other.hacking_difficulty and 
            self.hacked_value == other.hacked_value and 
            self.risk_factor == other.risk_factor
        )