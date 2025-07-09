from appv2.collections.coordinate_holders_collection import CoordinateHoldersCollection
from appv2.core.vectors import Vec2
from appv2.engine.grid.types import PlaceToPositionResult
from appv2.protocols.engine.grid.cell_protocol import CellProtocol
from appv2.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class Cell(CellProtocol):
    def __init__(self, coordinates: Vec2):
        self.coordinates = coordinates
        self.coordinate_holders: CoordinateHoldersCollection = CoordinateHoldersCollection()

    def remove(self, coordinate_holder: CoordinateHolderProtocol) -> bool:
        return True if self.coordinate_holders.pop(coordinate_holder.name, None) is not None else False


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
