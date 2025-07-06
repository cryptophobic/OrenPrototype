from typing import TYPE_CHECKING

from app.helpers.vectors import Vec2
from .actor import Actor
from .body import Body
from .shape import Shape

if TYPE_CHECKING:
    from ...behaviours.coordinate_holder.moveable import Moveable


class CoordinateHolder(Actor):
    def __init__(self, body: Body, shape: Shape, coordinates: Vec2, name: str = None):
        super().__init__(name=name)
        self.body: Body = body
        self.shape: Shape = shape
        self.coordinates: Vec2 = coordinates
        
        # Add moveable behaviour to all coordinate holders
        from ...config import Behaviours
        self.add_behaviour_from_enum(Behaviours.MOVEABLE)

    def blocks(self, other: 'CoordinateHolder') -> bool:
        return self.body.collision_matrix.blocks(other.body.collision_matrix)

    def overlaps(self, other: 'CoordinateHolder') -> bool:
        return self.body.collision_matrix.overlaps(other.body.collision_matrix)
