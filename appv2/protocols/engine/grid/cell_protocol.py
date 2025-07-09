from typing import Protocol
from appv2.core.vectors import Vec2
from appv2.engine.grid.types import PlaceToPositionResult
from appv2.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class CellProtocol(Protocol):
    coordinates: Vec2

    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: Vec2) -> PlaceToPositionResult: ...
    def remove(self, coordinate_holder: CoordinateHolderProtocol) -> bool: ...
    def is_occupied(self, coordinate_holder: CoordinateHolderProtocol) -> bool: ...
