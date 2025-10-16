from typing import Self

from app.components.geometry.shape import Shape
from app.components.physics.body import Body
from app.core.event_bus.bus import Strategy
from app.core.event_bus.events import Events
import app.core.event_bus.types as event_types
from app.core.event_bus.types import ObjectTypes
from app.core.types import MapLayer
from app.core.vectors import CustomVec2i, CustomVec2f
from app.components.objects.actor import Actor
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol

class CoordinateHolder(Actor, CoordinateHolderProtocol):
    def __init__(self, body: Body, shape: Shape, coordinates: CustomVec2i, name: str = None):
        super().__init__(name=name)
        self.body: Body = body
        self.shape: Shape = shape
        self.velocity: CustomVec2f = CustomVec2f.zero()
        self.intent_velocity: CustomVec2f = CustomVec2f.zero()
        self.coordinates: CustomVec2i = coordinates
        self.facing_direction: CustomVec2i = CustomVec2i.down()
        self.event_bus.subscribe_component(Events.ShapeAnimationUpdate, self.sprite_animation_emitter)

    def activate(self) -> None:
        self.event_bus.emit(
            Events.RegisterSprite,
            event_types.RegisterObjectPayload(
                object_name=self.name,
                object_type=ObjectTypes.ANIMATED if self.shape.animations else ObjectTypes.STATIC,
                coordinates=self.coordinates,
                z_index=MapLayer.OBJECTS,
                icon_path=self.shape.icon_path,
                animations=self.shape.get_current_animation(),
            ),
            Strategy.FirstWin,
        )
        self.is_active = True



    def sprite_animation_emitter(self, payload: event_types.ShapeAnimationUpdatePayload) -> None:
        self.event_bus.emit(Events.SpriteAnimationUpdate, event_types.SpriteAnimationUpdatePayload(self.name, payload.animation))

    def blocks(self, other: Self) -> bool:
        return self.body.collision_matrix.blocks(other.body.collision_matrix)

    def overlaps(self, other: Self) -> bool:
        return self.body.collision_matrix.overlaps(other.body.collision_matrix)
