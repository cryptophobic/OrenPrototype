from typing import Self

from app.core.event_bus.events import Events
import app.core.event_bus.types as event_types
from app.core.geometry.shape import Shape
from app.core.physics.body import Body
from app.core.vectors import CustomVec2i, CustomVec2f
from app.objects.actor import Actor
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class CoordinateHolder(Actor, CoordinateHolderProtocol):
    def __init__(self, body: Body, shape: Shape, coordinates: CustomVec2i, name: str = None):
        super().__init__(name=name)
        self.body: Body = body
        self.shape: Shape = shape
        self.velocity: CustomVec2f = CustomVec2f.zero()
        self.intent_velocity: CustomVec2f = CustomVec2f.zero()
        self.coordinates: CustomVec2i = coordinates

    def activate(self) -> None:
        self.event_bus.emit(
            Events.RegisterCoordinateHolder,
            event_types.RegisterCoordinateHolderPayload(
                object_name=self.name,
                object_type=event_types.ObjectTypes.ANIMATED if self.shape.animations else event_types.ObjectTypes.STATIC,
                coordinates=self.coordinates,
                icon_path=self.shape.icon_path,
                animations=self.shape.get_textures(),
            )
        )
        super().activate()

    def deactivate(self) -> None:
        # TODO: send deactivation event instead of unregister
        self.event_bus.emit(Events.UnregisterCoordinateHolder, event_types.UnregisterObjectPayload(object_name=self.name))
        super().deactivate()

    def delete(self) -> None:
        self.event_bus.emit(Events.UnregisterCoordinateHolder, event_types.UnregisterObjectPayload(object_name=self.name))
        super().delete()

    def blocks(self, other: Self) -> bool:
        return self.body.collision_matrix.blocks(other.body.collision_matrix)

    def overlaps(self, other: Self) -> bool:
        return self.body.collision_matrix.overlaps(other.body.collision_matrix)
