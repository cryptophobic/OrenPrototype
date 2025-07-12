from typing import Protocol

from app.collections.coordinate_holders_collection import CoordinateHoldersCollection
from app.core.vectors import Vec2
from app.engine.grid.types import PlaceToPositionResult
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class CellProtocol(Protocol):
    coordinates: Vec2
    coordinate_holders: CoordinateHoldersCollection

    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: Vec2) -> PlaceToPositionResult: ...
    def remove(self, coordinate_holder: CoordinateHolderProtocol) -> bool: ...
    def is_occupied(self, coordinate_holder: CoordinateHolderProtocol) -> bool: ...
