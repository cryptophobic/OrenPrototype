from app.objects.grid import Grid


class GridContext:
    def __init__(self):
        self.grid: Grid = Grid()

    def load_grid(self, width: int, height: int):
        self.grid = Grid(width=width, height=height)
        pass
