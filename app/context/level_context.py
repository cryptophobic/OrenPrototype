from app.engine.grid import Grid
from app.maps.level import Level


class LevelContext:
    def __init__(self):
        self.grid: Grid = Grid()

    def load_level(self, level: Level):
        pass
