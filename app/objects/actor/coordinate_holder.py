from app.helpers.vectors import Vec2
from .actor import Actor
from .body import Body
from .shape import Shape


class CoordinateHolder(Actor):
    def __init__(self, body: Body, shape: Shape, coordinates: Vec2, name: str = None):
        super().__init__(name=name)
        self.body: Body = body
        self.shape: Shape = shape
        self.coordinates: Vec2 = coordinates

    def blocks(self, other: 'CoordinateHolder') -> bool:
        return self.body.collision_matrix.blocks(other.body.collision_matrix)

    def overlaps(self, other: 'CoordinateHolder') -> bool:
        return self.body.collision_matrix.overlaps(other.body.collision_matrix)
