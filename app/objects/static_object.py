from app.core.geometry.shape import Shape
from app.core.physics.body import Body
from app.core.vectors import CustomVec2i
from app.objects.coordinate_holder import CoordinateHolder
from app.protocols.objects.static_object_protocol import StaticObjectProtocol


class StaticObject(CoordinateHolder, StaticObjectProtocol):
    def __init__(self,
                 body: Body,
                 shape: Shape,
                 coordinates: CustomVec2i,
                 height: int = 0,
                 weight: int = 0,
                 name: str = None
                 ):
        super().__init__(coordinates=coordinates, body=body, shape=shape, name=name)
        self.height = height
        self.weight = weight
