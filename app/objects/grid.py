from .actor.coordinate_holder import CoordinateHolder
from .actor.static_object import StaticObject
from .coordinate_holders_collection import CoordinateHoldersCollection
from .static_objects_collection import StaticObjectsCollection
from ..helpers.vectors import Vec2


class Cell:
    def __init__(self, coordinates: Vec2, static_objects: StaticObjectsCollection = None):
        self.coordinates = coordinates
        self.static_objects: StaticObjectsCollection = static_objects or StaticObjectsCollection()
        self.coordinate_holders: CoordinateHoldersCollection = CoordinateHoldersCollection()

    def remove_unit(self, coordinate_holder: CoordinateHolder) -> bool:
        if isinstance(coordinate_holder, StaticObject):
            return True if self.static_objects.pop(coordinate_holder.name, None) is not None else False

        return True if self.coordinate_holders.pop(coordinate_holder.name, None) is not None else False


    def place_unit(self, coordinate_holder: CoordinateHolder) -> bool:
        blocked = self.coordinate_holders.get_blocking_actors(coordinate_holder)
        if blocked:
            return False

        overlapped = self.coordinate_holders.get_overlapping_actors(coordinate_holder)
        for name, overlapping_coordinate_holder in overlapped.items():
            # TODO: send a message through the event bus.
            pass

        self.coordinate_holders[coordinate_holder.name] = coordinate_holder

        return True

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

    def place_unit(self, coordinate_holder: CoordinateHolder) -> bool:
        cell = self.get_cell(coordinate_holder.coordinates)
        return cell.place_unit(coordinate_holder) if cell else False

    def remove_unit(self, coordinate_holder: CoordinateHolder) -> bool:
        coordinates = coordinate_holder.coordinates
        cell = self.get_cell(coordinates)
        return cell.remove_unit(coordinate_holder) if cell else False

    def move_unit(self, coordinate_holder: CoordinateHolder, to_place: Vec2) -> bool:
        cell = self.get_cell(to_place)
        if not cell or cell.is_occupied(coordinate_holder):
            return False

        self.remove_unit(coordinate_holder)
        coordinate_holder.coordinates = to_place
        self.place_unit(coordinate_holder)
        return True