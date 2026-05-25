from dataclasses import dataclass


@dataclass
class Piazzamento:
    driverId: int
    position: int

    def __hash__(self):
        return hash((self.driverId, self.position))


    def __eq__(self, other):
        return (self.driverId, self.position) == (other.driverId, other.position)
