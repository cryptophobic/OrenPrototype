from app.object.static_object import StaticObject
from engine.unit import Pawn
from ui.actors.vectors import Vec2


class Cell:
    def __init__(self, coordinates: Vec2, static_objects: set[StaticObject] = None):
        self.coordinates = coordinates
        self.static_objects: set[StaticObject] = static_objects or set()
        self.pawn: set[Pawn] = set()

class Grid:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.cells: list[list[Cell]] = []
        # self.width = width
        # self.height = height
        # self.cells = [[Cell(Vec2(x=x, y=y)) for x in range(width)] for y in range(height)]

    def get_cell(self, coordinates: Vec2) -> Cell | None:
        if 0 <= coordinates.x < self.width and 0 <= coordinates.y < self.height:
            return self.cells[coordinates.y][coordinates.x]
        return None

    def place_unit(self, unit: Pawn) -> bool:
        coordinates = unit.actor.coordinates
        cell = self.get_cell(coordinates)
        if cell and not cell.is_occupied():
            cell.unit = unit
            unit.actor.position = coordinates
            return True
        return False

    def remove_unit(self, coordinates: Vec2) -> bool:
        cell = self.get_cell(coordinates)
        if cell and cell.unit:
            cell.unit = None
            return True
        return False

    def move_unit(self, from_place: Vec2, to_place: Vec2) -> bool:
        from_cell = self.get_cell(from_place)
        to_cell = self.get_cell(to_place)
        if from_cell and to_cell and from_cell.unit and not to_cell.is_occupied():
            to_cell.unit = from_cell.unit
            to_cell.unit.actor.position = to_place
            from_cell.unit = None
            return True
        return False
