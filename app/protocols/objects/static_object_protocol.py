from typing import runtime_checkable, Protocol

from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


@runtime_checkable
class StaticObjectProtocol(CoordinateHolderProtocol, Protocol):
    """Protocol for static objects with physical properties."""

    height: int
    weight: int
