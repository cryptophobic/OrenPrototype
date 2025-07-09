from typing import runtime_checkable, Protocol, Self

from appv2.core.geometry.shape import Shape
from appv2.core.physics.body import Body
from appv2.core.vectors import Vec2
from actor_protocol import ActorProtocol


@runtime_checkable
class CoordinateHolderProtocol(ActorProtocol, Protocol):
    """Protocol for objects that have coordinates, body and shape. Not body-shame, but body and shaPe"""

    body: Body
    shape: Shape
    coordinates: Vec2

    def blocks(self, other: Self) -> bool: ...
    def overlaps(self, other: Self) -> bool: ...
