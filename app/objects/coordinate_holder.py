from typing import Self

from app.core.geometry.shape import Shape
from app.core.physics.body import Body
from app.core.vectors import CustomVec2
from app.objects.actor import Actor
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class CoordinateHolder(Actor, CoordinateHolderProtocol):
    def __init__(self, body: Body, shape: Shape, coordinates: CustomVec2, name: str = None):
        super().__init__(name=name)
        self.body: Body = body
        self.shape: Shape = shape
        self.coordinates: CustomVec2 = coordinates

    def blocks(self, other: Self) -> bool:
        return self.body.collision_matrix.blocks(other.body.collision_matrix)

    def overlaps(self, other: Self) -> bool:
        return self.body.collision_matrix.overlaps(other.body.collision_matrix)
