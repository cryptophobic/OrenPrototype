from typing import Optional

from app.config import NpcAnimations, CommonAnimations
from app.core.collection_base import CollectionBase
from app.protocols.collections.animation_collection_protocol import AnimationCollectionProtocol
from app.registry.animation_registry import LoadedAnimation, get_animation_registry


class AnimationCollection(CollectionBase[CommonAnimations, NpcAnimations | LoadedAnimation], AnimationCollectionProtocol):
    def get(self, key: CommonAnimations) -> Optional[LoadedAnimation]:
        value = super().get(key)

        if isinstance(value, NpcAnimations):
            animation = get_animation_registry().get(value)
            self.items[key] = animation
            return animation

        return value

    def set(self, key: CommonAnimations, item: NpcAnimations) -> None:
        self.items[key] = item

    def _ensure_loaded(self, item: CommonAnimations) -> LoadedAnimation:
        loaded = self.get(item)
        if loaded is None:
            raise ValueError(f"Animation {item} not found in registry")
        return loaded
