from pathlib import Path

from arcade import Texture

from app.collections.animation_collection import AnimationCollection
from app.config import UnitStates
from app.components.component import Component
from app.components.geometry.types import Orientations
from app.protocols.collections.animation_collection_protocol import AnimationCollectionProtocol


class Shape(Component):
    def __init__(self, icon_path: Path):
        super().__init__()
        self.icon_path: Path = icon_path
        self.animations: AnimationCollectionProtocol = AnimationCollection()
        self.current_animation: UnitStates = UnitStates.IDLE
        self.orientation: Orientations = Orientations.FRONT
        pass

    def get_textures(self) -> list[Texture]:
        return self.animations.get_direction(self.current_animation, self.orientation)
