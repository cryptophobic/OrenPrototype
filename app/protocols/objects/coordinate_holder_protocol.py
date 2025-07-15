from typing import runtime_checkable, Protocol, Self

from app.core.geometry.shape import Shape
from app.core.physics.body import Body
from app.core.vectors import CustomVec2
from app.protocols.objects.actor_protocol import ActorProtocol


@runtime_checkable
class CoordinateHolderProtocol(ActorProtocol, Protocol):
    """Protocol for objects that have coordinates, body and shape. Not body-shame, but body and shaPe"""

    body: Body
    shape: Shape
    coordinates: CustomVec2

    def blocks(self, other: Self) -> bool: ...
    def overlaps(self, other: Self) -> bool: ...
