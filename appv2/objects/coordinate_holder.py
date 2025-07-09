from typing import Self

from actor import Actor
from appv2.core.geometry.shape import Shape
from appv2.core.physics.body import Body
from appv2.core.vectors import Vec2
from appv2.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class CoordinateHolder(Actor, CoordinateHolderProtocol):
    def __init__(self, body: Body, shape: Shape, coordinates: Vec2, name: str = None):
        super().__init__(name=name)
        self.body: Body = body
        self.shape: Shape = shape
        self.coordinates: Vec2 = coordinates

    def blocks(self, other: Self) -> bool:
        return self.body.collision_matrix.blocks(other.body.collision_matrix)

    def overlaps(self, other: Self) -> bool:
        return self.body.collision_matrix.overlaps(other.body.collision_matrix)
