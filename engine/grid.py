class Cell:
    def __init__(self, x, y, height=0):
        self.x = x
        self.y = y
        self.height = height
        self.unit = None       # Instance of Unit or None
        self.obstacle = False  # True if this cell has an obstacle
        self.selected = False

    def is_occupied(self):
        return self.unit is not None or self.obstacle


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y) for x in range(width)] for y in range(height)]

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

    def place_unit(self, unit, x, y):
        cell = self.get_cell(x, y)
        if cell and not cell.is_occupied():
            cell.unit = unit
            unit.position = (x, y)
            return True
        return False

    def remove_unit(self, x, y):
        cell = self.get_cell(x, y)
        if cell and cell.unit:
            cell.unit = None
            return True
        return False

    def move_unit(self, from_x, from_y, to_x, to_y):
        from_cell = self.get_cell(from_x, from_y)
        to_cell = self.get_cell(to_x, to_y)
        if from_cell and to_cell and from_cell.unit and not to_cell.is_occupied():
            to_cell.unit = from_cell.unit
            to_cell.unit.position = (to_x, to_y)
            from_cell.unit = None
            return True
        return False
