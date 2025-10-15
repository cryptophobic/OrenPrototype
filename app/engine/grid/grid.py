import app.core.event_bus.types as event_types
from app.components.component import Component
from app.core.event_bus.bus import bus
from app.core.event_bus.events import Events
from app.core.vectors import CustomVec2i
from app.engine.grid.cell import Cell
from app.engine.grid.types import PlaceToPositionResult
from app.protocols.engine.grid.grid_protocol import GridProtocol
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class Grid(Component, GridProtocol):
    def __init__(self, width = 0, height = 0):
        super().__init__()
        self.width = width
        self.height = height
        self.event_bus = bus
        self.cells = [[Cell(CustomVec2i(x=x, y=y)) for x in range(width)] for y in range(height)]

    def get_cell(self, coordinates: CustomVec2i) -> Cell | None:
        if 0 <= coordinates.x < self.width and 0 <= coordinates.y < self.height:
            return self.cells[coordinates.y][coordinates.x]
        return None

    def place(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> PlaceToPositionResult:
        result = self._place(coordinate_holder, to_place)
        if result.placed:
            self.event_bus.emit(
                Events.RegisterCoordinateHolder,
                event_types.RegisterObjectPayload(
                    object_name=coordinate_holder.name,
                    object_type=event_types.ObjectTypes.ANIMATED if coordinate_holder.shape.animations else event_types.ObjectTypes.STATIC,
                    coordinates=coordinate_holder.coordinates,
                    icon_path=coordinate_holder.shape.icon_path,
                    animations=coordinate_holder.shape.get_textures(),
                )
            )

        return result

    def _place(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> PlaceToPositionResult:
        cell = self.get_cell(to_place)
        return cell.place(coordinate_holder, to_place) if cell else PlaceToPositionResult(placed=False)

    def remove(self, coordinate_holder: CoordinateHolderProtocol, from_place: CustomVec2i) -> bool:
        cell = self.get_cell(from_place)
        if cell:
            self.event_bus.emit(
                Events.UnregisterCoordinateHolder,
                event_types.ObjectPayload(
                    object_name=coordinate_holder.name,
                )
            )
            return cell.remove(coordinate_holder)
        else:
            return False

    def is_may_be_occupied(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> PlaceToPositionResult:
        cell = self.get_cell(to_place)
        return cell.is_able_to_occupy(coordinate_holder, to_place) if cell else PlaceToPositionResult(placed=False)

    def move(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> PlaceToPositionResult:
        from_place = coordinate_holder.coordinates
        result = self._place(coordinate_holder, to_place)
        if result.placed:
            self.event_bus.emit(
                Events.MoveCoordinateHolder,
                event_types.ObjectPositionPayload(
                    object_name=coordinate_holder.name,
                    coordinates=to_place,
                )
            )
            self.remove(coordinate_holder, from_place)
        return result
