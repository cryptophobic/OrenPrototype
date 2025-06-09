from app.helpers.vectors import Vec2
from app.object.actor import Actor
from .body import Body


class CoordinateHolder(Actor):
    def __init__(self, body: Body, coordinates: Vec2):
        super().__init__()
        self.body: Body = body
        self.coordinates: Vec2 = coordinates
