from typing import runtime_checkable, Protocol

from app.objects.types import UnitStats
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


@runtime_checkable
class UnitProtocol(CoordinateHolderProtocol, Protocol):
    """Protocol for units that have stats and can perform actions."""

    stats: UnitStats
