from dataclasses import dataclass
from enum import Enum, auto

from ui.actors.shape import Shape
from ui.actors.vectors import Vec2

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
                 coordinates: Vec2 = Vec2(x=0, y=0),
                 velocity: Vec2 = Vec2(x=0, y=0),
                 collision_matrix: CollisionMatrix = CollisionMatrix()):
        self.shape: Shape = shape
        self.coordinates: Vec2 = coordinates
        self.velocity: Vec2 = velocity
        self.collision_matrix: CollisionMatrix = collision_matrix
        pass

    def is_dirty(self):
        return self.velocity.is_dirty()