from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.components.component import Component
from app.core.vectors import CustomVec2i
from app.engine.grid.types import PlaceToPositionResult
from app.protocols.engine.grid.cell_protocol import CellProtocol
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class Cell(Component, CellProtocol):
    def __init__(self, coordinates: CustomVec2i):
        super().__init__()
        self.coordinates = coordinates
        self.coordinate_holders: CoordinateHolderCollection = CoordinateHolderCollection()

    def remove(self, coordinate_holder: CoordinateHolderProtocol) -> bool:
        return self.coordinate_holders.remove(coordinate_holder.name)

    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> PlaceToPositionResult:
        place_to_position_result = self.is_able_to_occupy(coordinate_holder, to_place)

        if place_to_position_result.placed:
            coordinate_holder.coordinates = to_place
            self.coordinate_holders.add(coordinate_holder)

        return place_to_position_result

    def is_able_to_occupy(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> PlaceToPositionResult:
        blocked = self.coordinate_holders.get_blocking_actors(coordinate_holder)
        if blocked:
            return PlaceToPositionResult(placed=False, blocked=blocked)

        overlapped = self.coordinate_holders.get_overlapping_actors(coordinate_holder)
        return PlaceToPositionResult(placed=True, overlapped=overlapped)
