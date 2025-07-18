from typing import Optional

from app.config import NpcAnimations
from app.protocols.core.collection_base_protocol import CollectionBaseProtocol
from app.registry.animation_registry import LoadedAnimation


class AnimationCollectionProtocol(CollectionBaseProtocol):
    def get(self, item: NpcAnimations) -> Optional[LoadedAnimation]: ...
    def set(self, item: NpcAnimations) -> None: ...
