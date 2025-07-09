from typing import Protocol
from appv2.core.vectors import Vec2
from appv2.engine.grid.types import PlaceToPositionResult
from appv2.protocols.engine.grid.cell_protocol import CellProtocol
from appv2.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class GridProtocol(Protocol):
    width: int
    height: int

    def get_cell(self, coordinates: Vec2) -> CellProtocol | None: ...
    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: Vec2) -> PlaceToPositionResult: ...
    def remove(self, coordinate_holder: CoordinateHolderProtocol, from_place: Vec2) -> bool: ...
    def move(self, coordinate_holder: CoordinateHolderProtocol, to_place: Vec2) -> PlaceToPositionResult: ...
