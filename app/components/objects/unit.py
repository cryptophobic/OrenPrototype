from app.components.geometry.shape import Shape
from app.components.physics.body import Body
from app.core.vectors import CustomVec2i
from app.components.objects.coordinate_holder import CoordinateHolder
from app.components.objects.types import UnitStats
from app.protocols.objects.unit_protocol import UnitProtocol


class Unit(CoordinateHolder, UnitProtocol):
    def __init__(self,
                 body: Body,
                 shape: Shape,
                 coordinates: CustomVec2i,
                 stats: UnitStats = UnitStats(),
                 name: str = None
                 ):
        super().__init__(body=body, shape=shape, coordinates=coordinates, name=name)
        self.stats: UnitStats = stats
