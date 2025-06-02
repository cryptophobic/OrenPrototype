from typing import List

from app.object.coordinate_holder import CoordinateHolder
from app.object.static_object import StaticObject
from app.engine.grid import Grid, Cell
from app.helpers.vectors import Vec2


class Level:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.pawns: List[CoordinateHolder] = []
        self.static_objects: List[StaticObject] = []
        self.grid.width = 0
        self.grid.height = 0

    def generate(self):
        self.grid.cells = [[Cell(Vec2(x=x, y=y)) for x in range(self.grid.width)] for y in range(self.grid.height)]
