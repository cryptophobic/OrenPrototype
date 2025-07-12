from app.core.geometry.shape import Shape
from app.core.physics.body import Body
from app.core.vectors import Vec2
from app.objects.coordinate_holder import CoordinateHolder
from app.objects.types import UnitStats
from app.protocols.objects.unit_protocol import UnitProtocol


class Unit(CoordinateHolder, UnitProtocol):
    def __init__(self,
                 body: Body,
                 shape: Shape,
                 coordinates: Vec2,
                 stats: UnitStats = UnitStats(),
                 name: str = None
                 ):
        super().__init__(body=body, shape=shape, coordinates=coordinates, name=name)
        self.stats: UnitStats = stats
