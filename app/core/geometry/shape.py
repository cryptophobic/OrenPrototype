from pathlib import Path

from arcade import Texture

from app.collections.animation_collection import AnimationCollection
from app.config import NpcAnimations, CommonAnimations
from app.core.geometry.types import Directions
from app.protocols.collections.animation_collection_protocol import AnimationCollectionProtocol


class Shape:
    def __init__(self, icon_path: Path):
        self.icon_path: Path = icon_path
        self.animations: AnimationCollectionProtocol = AnimationCollection()
        self.animation_mapping: dict[CommonAnimations, NpcAnimations] = {}
        self.current_animation: CommonAnimations = CommonAnimations.IDLE
        self.direction: Directions = Directions.FRONT
        pass

    def get_textures(self) -> list[Texture]:
        return self.animations.get_direction(self.current_animation, self.direction)
