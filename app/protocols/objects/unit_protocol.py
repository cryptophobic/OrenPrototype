from typing import runtime_checkable, Protocol

from app.components.objects.types import UnitStats
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


@runtime_checkable
class UnitProtocol(CoordinateHolderProtocol, Protocol):
    stats: UnitStats
