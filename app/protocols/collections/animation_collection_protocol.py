from typing import Optional

from app.config import NpcAnimations, CommonAnimations
from app.protocols.core.collection_base_protocol import CollectionBaseProtocol
from app.registry.animation_registry import LoadedAnimation


class AnimationCollectionProtocol(CollectionBaseProtocol):
    def get(self, key: CommonAnimations) -> Optional[LoadedAnimation]: ...
    def set(self, key: CommonAnimations, item: NpcAnimations) -> None: ...
