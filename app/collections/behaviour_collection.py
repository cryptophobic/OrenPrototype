from typing import Self, Optional

from app.engine.message_broker.types import MessageTypes
from app.config import Behaviours
from app.core.collection_base import CollectionBase
from app.protocols.behaviours.behaviour_protocol import BehaviourProtocol
from app.registry.behaviour_registry import get_registry


class BehaviourCollection(CollectionBase[Behaviours, Behaviours | BehaviourProtocol]):
    def __init__(self, items: Optional[CollectionBase[Behaviours, Behaviours | BehaviourProtocol]] = None):
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
