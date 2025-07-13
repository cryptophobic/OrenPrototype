from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.core.vectors import Vec2
from app.engine.grid.cell import Cell
from app.engine.grid.types import PlaceToPositionResult
from app.protocols.engine.grid.grid_protocol import GridProtocol
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class Grid(GridProtocol):
    def __init__(self, width = 0, height = 0):
        self.width = width
        self.height = height
        self.cells = [[Cell(Vec2(x=x, y=y)) for x in range(width)] for y in range(height)]

    def get_cell(self, coordinates: Vec2) -> Cell | None:
        if 0 <= coordinates.x < self.width and 0 <= coordinates.y < self.height:
            return self.cells[coordinates.y][coordinates.x]
        return None

    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: Vec2) -> PlaceToPositionResult:
        cell = self.get_cell(to_place)
        return cell.place(coordinate_holder, to_place) if cell else PlaceToPositionResult(placed=False)

    def remove(self, coordinate_holder: CoordinateHolderProtocol, from_place: Vec2) -> bool:
        cell = self.get_cell(from_place)
        return cell.remove(coordinate_holder) if cell else False

    def move(self, coordinate_holder: CoordinateHolderProtocol, to_place: Vec2) -> PlaceToPositionResult:
        from_place = coordinate_holder.coordinates
        result = self.place(coordinate_holder, to_place)
        if result.placed:
            self.remove(coordinate_holder, from_place)
        return result
