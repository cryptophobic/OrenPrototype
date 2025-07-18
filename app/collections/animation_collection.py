from typing import Optional

from app.config import NpcAnimations
from app.core.collection_base import CollectionBase
from app.protocols.collections.animation_collection_protocol import AnimationCollectionProtocol
from app.registry.animation_registry import LoadedAnimation, get_animation_registry


class AnimationCollection(CollectionBase[NpcAnimations, NpcAnimations | LoadedAnimation], AnimationCollectionProtocol):
    def get(self, item: NpcAnimations) -> Optional[LoadedAnimation]:
        value = super().get(item)

        if isinstance(value, NpcAnimations):
            animation = get_animation_registry().get(value)
            self.items[item] = animation
            return animation

        return value

    def set(self, item: NpcAnimations) -> None:
        self.items[item] = item

    def _ensure_loaded(self, item: NpcAnimations) -> LoadedAnimation:
        loaded = self.get(item)
        if loaded is None:
            raise ValueError(f"Animation {item} not found in registry")
        return loaded
