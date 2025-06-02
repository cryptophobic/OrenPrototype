from app.helpers.vectors import Vec2
from app.object.coordinate_holder import CoordinateHolder


class Unit(CoordinateHolder):
    def __init__(self, coordinates: Vec2):
        super().__init__(coordinates)