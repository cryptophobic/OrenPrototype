from typing import Protocol

from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.core.vectors import CustomVec2i
from app.engine.grid.types import PlaceToPositionResult
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class CellProtocol(Protocol):
    coordinates: CustomVec2i
    coordinate_holders: CoordinateHolderCollection

    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> PlaceToPositionResult: ...
    def remove(self, coordinate_holder: CoordinateHolderProtocol) -> bool: ...
    def is_able_to_occupy(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> PlaceToPositionResult: ...
