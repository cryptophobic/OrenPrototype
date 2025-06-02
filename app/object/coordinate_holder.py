from app.helpers.vectors import Vec2
from app.object.actor import Actor


class CoordinateHolder(Actor):
    def __init__(self, coordinates: Vec2):
        super().__init__()
        self.coordinates = coordinates
