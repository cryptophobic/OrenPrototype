from typing import Protocol
from app.core.vectors import CustomVec2i
from app.engine.grid.types import PlaceToPositionResult
from app.protocols.engine.grid.cell_protocol import CellProtocol
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class GridProtocol(Protocol):
    width: int
    height: int

    def get_cell(self, coordinates: CustomVec2i) -> CellProtocol | None: ...
    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> PlaceToPositionResult: ...
    def remove(self, coordinate_holder: CoordinateHolderProtocol, from_place: CustomVec2i) -> bool: ...
    def move(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> PlaceToPositionResult: ...
