from pathlib import Path

from arcade import Texture

from app.collections.animation_collection import AnimationCollection
from app.config import NpcAnimations, CommonAnimations
from app.protocols.collections.animation_collection_protocol import AnimationCollectionProtocol


class Shape:
    def __init__(self, icon_path: Path):
        self.icon_path: Path = icon_path
        self.animations: AnimationCollectionProtocol = AnimationCollection()
        self.animation_mapping: dict[CommonAnimations, NpcAnimations] = {}
        self.current_animation: CommonAnimations = CommonAnimations.IDLE
        self.direction = 'front'
        pass

    # TODO: remove the playground
    def get_textures(self) -> list[Texture]:
        match self.direction:
            case 'front':
                return self.animations.get(self.current_animation).front
            case 'back':
                return self.animations.get(self.current_animation).back
            case 'left':
                return self.animations.get(self.current_animation).left
            case 'right':
                return self.animations.get(self.current_animation).right
        return self.animations.get(self.current_animation).front
