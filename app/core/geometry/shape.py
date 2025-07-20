from pathlib import Path

from app.collections.animation_collection import AnimationCollection
from app.config import NpcAnimations, CommonAnimations
from app.protocols.collections.animation_collection_protocol import AnimationCollectionProtocol


class Shape:
    def __init__(self, icon_path: Path):
        self.icon_path: Path = icon_path
        self.animations: AnimationCollectionProtocol = AnimationCollection()
        self.animation_mapping: dict[CommonAnimations, NpcAnimations] = {}
        self.current_animation: CommonAnimations = CommonAnimations.IDLE
        pass
