from pathlib import Path
from typing import Optional

from arcade import Texture

from app.collections.animation_collection import AnimationCollection
from app.config import UnitStates
from app.components.component import Component
from app.components.geometry.types import Orientations
from app.core.event_bus.bus import bus, Strategy
from app.core.event_bus.events import Events
from app.core.event_bus.types import ShapeAnimationUpdatePayload
from app.protocols.collections.animation_collection_protocol import AnimationCollectionProtocol


class Shape(Component):
    def __init__(self, icon_path: Path):
        super().__init__()
        self.event_bus = bus
        self.icon_path: Path = icon_path
        self.animations: AnimationCollectionProtocol = AnimationCollection()
        self.current_animation: Optional[list[Texture]] = None
        pass

    def set_current_animation(self, state: UnitStates, orientation: Orientations) -> None:
        self.current_animation = self.animations.get_direction(state, orientation)
        bus.emit(Events.ShapeAnimationUpdate, ShapeAnimationUpdatePayload(self.current_animation), Strategy.FirstWin)

    def get_current_animation(self) -> list[Texture]:
        return self.current_animation
