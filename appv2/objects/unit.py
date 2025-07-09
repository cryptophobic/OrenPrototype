from appv2.core.geometry.shape import Shape
from appv2.core.physics.body import Body
from appv2.core.vectors import Vec2
from appv2.objects.coordinate_holder import CoordinateHolder
from appv2.objects.types import UnitStats
from appv2.protocols.objects.unit_protocol import UnitProtocol


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
