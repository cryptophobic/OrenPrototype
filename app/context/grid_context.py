from app.engine.grid import Grid
from app.maps.level import Level


class GridContext:
    def __init__(self):
        self.grid: Grid = Grid()

    def load_grid(self, width: int, height: int):
        self.grid = Grid(width=width, height=height)
        pass
