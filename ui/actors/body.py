from dataclasses import dataclass
from enum import Enum, auto

from ui.actors.shape import Shape

class CollisionResponse(Enum):
    BLOCK = auto()
    OVERLAP = auto()
    IGNORE = auto()

@dataclass
class CollisionMatrix:
    response: CollisionResponse

    def overlaps(self, other: 'CollisionMatrix') -> bool:
        if CollisionResponse.IGNORE in (self.response, other.response):
            return False

        if CollisionResponse.OVERLAP in (self.response, other.response):
            return True

        return False

    def blocks(self, other: 'CollisionMatrix') -> bool:
        return self.response == CollisionResponse.BLOCK and other.response == CollisionResponse.BLOCK


class Body:
    def __init__(self,
                 shape: Shape = None,
                 collision_matrix: CollisionMatrix = CollisionMatrix(response=CollisionResponse.IGNORE),):
        self.shape: Shape = shape
        self.collision_matrix: CollisionMatrix = collision_matrix
        pass

    def is_solid(self) -> bool:
        return self.collision_matrix.response == CollisionResponse.BLOCK

    def is_soft(self) -> bool:
        return self.collision_matrix.response == CollisionResponse.OVERLAP
