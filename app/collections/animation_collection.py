from typing import Optional

from arcade import Texture

from app.config import NpcAnimations, UnitStates
from app.core.collection_base import CollectionBase
from app.core.geometry.types import Directions
from app.protocols.collections.animation_collection_protocol import AnimationCollectionProtocol
from app.registry.animation_registry import LoadedAnimation, get_animation_registry


class AnimationCollection(CollectionBase[UnitStates, NpcAnimations | LoadedAnimation], AnimationCollectionProtocol):
    def get(self, key: UnitStates) -> Optional[LoadedAnimation]:
        value = super().get(key)

        if isinstance(value, NpcAnimations):
            animation = get_animation_registry().get(value)
            self.items[key] = animation
            return animation

        return value

    def get_direction(self, key: UnitStates, direction: Directions) -> Optional[list[Texture]]:
        loaded_animation = self._ensure_loaded(key)

        if direction == Directions.FRONT:
            return loaded_animation.front
        elif direction == Directions.BACK:
            return loaded_animation.back
        elif direction == Directions.LEFT:
            return loaded_animation.left
        elif direction == Directions.RIGHT:
            return loaded_animation.right

        return loaded_animation.front


    def set(self, key: UnitStates, item: NpcAnimations) -> None:
        self.items[key] = item

    def _ensure_loaded(self, item: UnitStates) -> LoadedAnimation:
        loaded = self.get(item)
        if loaded is None:
            raise ValueError(f"Animation {item} not found in registry")
        return loaded
