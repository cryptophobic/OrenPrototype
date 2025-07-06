from dataclasses import dataclass, field

from .actor.coordinate_holder import CoordinateHolder
from .actor.static_object import StaticObject
from .coordinate_holders_collection import CoordinateHoldersCollection
from .static_objects_collection import StaticObjectsCollection
from ..helpers.vectors import Vec2

@dataclass
class PlaceToPositionResult:
    placed: bool = False
    blocked: CoordinateHoldersCollection = field(default_factory=CoordinateHoldersCollection)
    overlapped: CoordinateHoldersCollection = field(default_factory=CoordinateHoldersCollection)

class Cell:
    def __init__(self, coordinates: Vec2):
        self.coordinates = coordinates
        self.static_objects: StaticObjectsCollection = StaticObjectsCollection()
        self.coordinate_holders: CoordinateHoldersCollection = CoordinateHoldersCollection()

    def remove_coordinate_holder(self, coordinate_holder: CoordinateHolder) -> bool:
        if isinstance(coordinate_holder, StaticObject):
            return True if self.static_objects.pop(coordinate_holder.name, None) is not None else False

        return True if self.coordinate_holders.pop(coordinate_holder.name, None) is not None else False


    def place_coordinate_holder(self, coordinate_holder: CoordinateHolder, to_place: Vec2) -> PlaceToPositionResult:
        blocked_list = []
        blocked = self.coordinate_holders.get_blocking_actors(coordinate_holder)
        if blocked:
            blocked_list.append(blocked)

        blocked = self.static_objects.get_blocking_actors(coordinate_holder)
        if blocked:
            blocked_list.append(blocked)

        if blocked_list:
            return PlaceToPositionResult(placed=False, blocked=CoordinateHoldersCollection.from_collections(blocked_list))

        overlapped_list = []
        overlapped = self.coordinate_holders.get_overlapping_actors(coordinate_holder)
        if overlapped:
            overlapped_list.append(overlapped)

        overlapped = self.static_objects.get_overlapping_actors(coordinate_holder)
        if overlapped:
            overlapped_list.append(overlapped)

        coordinate_holder.coordinates = to_place

        if isinstance(coordinate_holder, StaticObject):
            self.static_objects.add(coordinate_holder)
        else:
            self.coordinate_holders.add(coordinate_holder)

        return PlaceToPositionResult(placed=True, blocked=CoordinateHoldersCollection.from_collections(overlapped_list))

    def is_occupied(self, coordinate_holder: CoordinateHolder) -> bool:
        return True if self.coordinate_holders.get_blocking_actors(coordinate_holder) else False

class Grid:
    def __init__(self, width = 0, height = 0):
        self.width = width
        self.height = height
        self.cells = [[Cell(Vec2(x=x, y=y)) for x in range(width)] for y in range(height)]

    def get_cell(self, coordinates: Vec2) -> Cell | None:
        if 0 <= coordinates.x < self.width and 0 <= coordinates.y < self.height:
            return self.cells[coordinates.y][coordinates.x]
        return None

    def place_coordinate_holder(self, coordinate_holder: CoordinateHolder, to_place: Vec2) -> PlaceToPositionResult:
        cell = self.get_cell(to_place)
        return cell.place_coordinate_holder(coordinate_holder, to_place) if cell else (False, CoordinateHoldersCollection())

    def remove_coordinate_holder(self, coordinate_holder: CoordinateHolder, from_place: Vec2) -> bool:
        cell = self.get_cell(from_place)
        return cell.remove_coordinate_holder(coordinate_holder) if cell else False

    def move_coordinate_holder(self, coordinate_holder: CoordinateHolder, to_place: Vec2) -> PlaceToPositionResult:
        from_place = coordinate_holder.coordinates
        result = self.place_coordinate_holder(coordinate_holder, to_place)
        if result.placed:
            self.remove_coordinate_holder(coordinate_holder, from_place)
        return result
