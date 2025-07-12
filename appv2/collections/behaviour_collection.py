from typing import Self, Optional

from appv2.engine.message_broker.types import MessageTypes
from appv2.config import Behaviours
from appv2.core.collection_base import CollectionBase
from appv2.protocols.behaviours.behaviour_protocol import BehaviourProtocol
from appv2.registry.behaviour_registry import get_registry


class BehaviourCollection(CollectionBase[Behaviours, Behaviours | BehaviourProtocol]):
    def __init__(self, items: CollectionBase[Behaviours, Behaviours | BehaviourProtocol]):
        super().__init__(items or {})

    def get(self, item: Behaviours) -> Optional[BehaviourProtocol]:
        value = super().get(item)

        if isinstance(value, Behaviours):
            behaviour = get_registry().get(value)
            self.items[item] = behaviour
            return behaviour

        return value

    def _ensure_loaded(self, item: Behaviours) -> BehaviourProtocol:
        loaded = self.get(item)
        if loaded is None:
            raise ValueError(f"Behaviour {item} not found in registry")
        return loaded

    def load_all(self) -> None:
        for key, value in list(self.items.items()):
            if isinstance(value, Behaviours):
                self.get(key)

    def can_respond_to(self, message_type: MessageTypes) -> Self:
        return type(self)(
            self.filter(
                lambda item: self._ensure_loaded(item).can_respond_to(message_type)
            )
        )
