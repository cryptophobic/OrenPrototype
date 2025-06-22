from app.helpers.vectors import Vec2
from .body import Body
from .coordinate_holder import CoordinateHolder
from .shape import Shape


class StaticObject(CoordinateHolder):
    def __init__(self,
                 body: Body,
                 shape: Shape,
                 coordinates: Vec2,
                 height: int = 0,
                 weight: int = 0,
                 name: str = None
                 ):
        super().__init__(coordinates=coordinates, body=body, shape=shape, name=name)
        self.height = height
        self.weight = weight
