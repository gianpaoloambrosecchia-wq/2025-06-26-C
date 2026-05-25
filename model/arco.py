from dataclasses import dataclass

from model.costruttore import Costruttore


@dataclass
class Arco:
    c1: Costruttore
    c2: Costruttore
    peso: int = 0

    def __hash__(self):
        return hash((self.c1, self.c2))

    def __eq__(self, other):
        return self.c1 == other.c1 and self.c2 == other.c2