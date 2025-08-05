from typing import Optional

from arcade import Texture

from app.config import NpcAnimations, CommonAnimations
from app.core.geometry.types import Directions
from app.protocols.core.collection_base_protocol import CollectionBaseProtocol
from app.registry.animation_registry import LoadedAnimation


class AnimationCollectionProtocol(CollectionBaseProtocol):
    def get(self, key: CommonAnimations) -> Optional[LoadedAnimation]: ...
    def get_direction(self, key: CommonAnimations, direction: Directions) -> Optional[list[Texture]]: ...
    def set(self, key: CommonAnimations, item: NpcAnimations) -> None: ...
