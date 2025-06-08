from app.helpers.vectors import Vec2


class Cell:
    def __init__(self, coordinates: Vec2, height=0):
        self.coordinates = coordinates
        self.height = height
        self.occupants = []  # Support multiple objects per cell
        self.selected = False

    def add_occupant(self, obj):
        """Add an object to this cell"""
        if obj not in self.occupants:
            self.occupants.append(obj)

    def remove_occupant(self, obj):
        """Remove an object from this cell"""
        if obj in self.occupants:
            self.occupants.remove(obj)

    def is_occupied(self) -> bool:
        """Check if cell has any occupants"""
        return len(self.occupants) > 0

    def can_accommodate(self, new_obj) -> bool:
        """Check if cell can accommodate new object (height-based logic)"""
        # For now, allow multiple occupants
        # Will implement height-based collision later
        return True

    def get_primary_unit(self):
        """Get the first unit-type occupant"""
        for occupant in self.occupants:
            if hasattr(occupant, 'stats'):  # Assume units have stats
                return occupant
        return None


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = [[Cell(Vec2(x=x, y=y)) for x in range(width)] for y in range(height)]

    def get_cell(self, coordinates: Vec2) -> Cell | None:
        """Get cell at coordinates"""
        if 0 <= coordinates.x < self.width and 0 <= coordinates.y < self.height:
            return self.cells[coordinates.y][coordinates.x]
        return None

    def place_object(self, obj, coordinates: Vec2) -> bool:
        """Place object at coordinates"""
        cell = self.get_cell(coordinates)
        if cell and cell.can_accommodate(obj):
            cell.add_occupant(obj)
            if hasattr(obj, 'position'):
                obj.position = coordinates
            return True
        return False

    def remove_object(self, obj, coordinates: Vec2) -> bool:
        """Remove object from coordinates"""
        cell = self.get_cell(coordinates)
        if cell:
            cell.remove_occupant(obj)
            return True
        return False

    def move_object(self, obj, from_pos: Vec2, to_pos: Vec2) -> bool:
        """Move object from one position to another"""
        from_cell = self.get_cell(from_pos)
        to_cell = self.get_cell(to_pos)
        
        if from_cell and to_cell and obj in from_cell.occupants:
            if to_cell.can_accommodate(obj):
                from_cell.remove_occupant(obj)
                to_cell.add_occupant(obj)
                if hasattr(obj, 'position'):
                    obj.position = to_pos
                return True
        return False

    def is_valid_position(self, coordinates: Vec2) -> bool:
        """Check if coordinates are within grid bounds"""
        return 0 <= coordinates.x < self.width and 0 <= coordinates.y < self.height

    def get_neighbors(self, coordinates: Vec2) -> list[Vec2]:
        """Get valid neighboring coordinates"""
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = Vec2(coordinates.x + dx, coordinates.y + dy)
            if self.is_valid_position(neighbor):
                neighbors.append(neighbor)
        return neighbors