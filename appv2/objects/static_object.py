from appv2.core.geometry.shape import Shape
from appv2.core.physics.body import Body
from appv2.core.vectors import Vec2
from appv2.objects.coordinate_holder import CoordinateHolder
from appv2.protocols.objects.static_object_protocol import StaticObjectProtocol


class StaticObject(CoordinateHolder, StaticObjectProtocol):
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
