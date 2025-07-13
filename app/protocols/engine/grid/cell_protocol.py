from typing import Protocol

from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.core.vectors import Vec2
from app.engine.grid.types import PlaceToPositionResult
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class CellProtocol(Protocol):
    coordinates: Vec2
    coordinate_holders: CoordinateHolderCollection

    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: Vec2) -> PlaceToPositionResult: ...
    def remove(self, coordinate_holder: CoordinateHolderProtocol) -> bool: ...
    def is_occupied(self, coordinate_holder: CoordinateHolderProtocol) -> bool: ...
