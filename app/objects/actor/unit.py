from dataclasses import dataclass

from .body import Body
from .shape import Shape
from ...helpers.vectors import Vec2
from .coordinate_holder import CoordinateHolder

@dataclass
class Stats:
    STR: int = 0
    DEX: int = 0
    CON: int = 0
    INT: int = 0
    WIS: int = 0
    CHA: int = 0
    HP: int = 0
    initiative: int = 0


class Unit(CoordinateHolder):
    def __init__(self,
                 body: Body,
                 shape: Shape,
                 coordinates: Vec2,
                 stats: Stats = Stats()
                 ):
        super().__init__(body=body, shape=shape, coordinates=coordinates)
        self.stats: Stats = stats
