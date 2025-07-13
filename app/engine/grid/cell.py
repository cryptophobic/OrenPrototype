from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.core.vectors import Vec2
from app.engine.grid.types import PlaceToPositionResult
from app.protocols.engine.grid.cell_protocol import CellProtocol
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class Cell(CellProtocol):
    def __init__(self, coordinates: Vec2):
        self.coordinates = coordinates
        self.coordinate_holders: CoordinateHolderCollection = CoordinateHolderCollection()

    def remove(self, coordinate_holder: CoordinateHolderProtocol) -> bool:
        return self.coordinate_holders.remove(coordinate_holder.name)


    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: Vec2) -> PlaceToPositionResult:
        blocked = self.coordinate_holders.get_blocking_actors(coordinate_holder)
        if blocked:
            return PlaceToPositionResult(placed=False, blocked=blocked)

        overlapped = self.coordinate_holders.get_overlapping_actors(coordinate_holder)

        coordinate_holder.coordinates = to_place

        self.coordinate_holders.add(coordinate_holder)

        return PlaceToPositionResult(placed=True, overlapped=overlapped)

    def is_occupied(self, coordinate_holder: CoordinateHolderProtocol) -> bool:
        return True if self.coordinate_holders.get_blocking_actors(coordinate_holder) else False
