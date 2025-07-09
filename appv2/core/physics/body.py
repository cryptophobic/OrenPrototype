from dataclasses import dataclass
from enum import Enum, auto
from typing import Self


class CollisionResponse(Enum):
    BLOCK = auto()
    OVERLAP = auto()
    IGNORE = auto()

@dataclass
class CollisionMatrix:
    response: CollisionResponse

    def overlaps(self, other: Self) -> bool:
        if CollisionResponse.IGNORE in (self.response, other.response):
            return False

        if CollisionResponse.OVERLAP in (self.response, other.response):
            return True

        return False

    def blocks(self, other: Self) -> bool:
        return self.response == CollisionResponse.BLOCK and other.response == CollisionResponse.BLOCK


class Body:
    def __init__(self,
                 collision_matrix: CollisionMatrix = CollisionMatrix(response=CollisionResponse.IGNORE),):
        self.collision_matrix: CollisionMatrix = collision_matrix
        pass

    def is_solid(self) -> bool:
        return self.collision_matrix.response == CollisionResponse.BLOCK

    def is_soft(self) -> bool:
        return self.collision_matrix.response == CollisionResponse.OVERLAP

    def is_hidden(self) -> bool:
        return self.collision_matrix.response == CollisionResponse.IGNORE
