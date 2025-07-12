from typing import Protocol
from app.core.vectors import Vec2
from app.engine.grid.types import PlaceToPositionResult
from app.protocols.engine.grid.cell_protocol import CellProtocol
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class GridProtocol(Protocol):
    width: int
    height: int

    def get_cell(self, coordinates: Vec2) -> CellProtocol | None: ...
    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: Vec2) -> PlaceToPositionResult: ...
    def remove(self, coordinate_holder: CoordinateHolderProtocol, from_place: Vec2) -> bool: ...
    def move(self, coordinate_holder: CoordinateHolderProtocol, to_place: Vec2) -> PlaceToPositionResult: ...
