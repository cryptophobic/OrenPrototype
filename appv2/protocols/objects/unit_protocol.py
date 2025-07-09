from typing import runtime_checkable, Protocol

from appv2.objects.types import UnitStats
from coordinate_holder_protocol import CoordinateHolderProtocol


@runtime_checkable
class UnitProtocol(CoordinateHolderProtocol, Protocol):
    """Protocol for units that have stats and can perform actions."""

    stats: UnitStats
