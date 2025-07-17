from typing import Self, Optional

from app.engine.message_broker.types import MessageTypes
from app.config import Behaviours
from app.core.collection_base import CollectionBase
from app.protocols.behaviours.behaviour_protocol import BehaviourProtocol
from app.protocols.collections.behaviour_collection_protocol import BehaviourCollectionProtocol
from app.registry.behaviour_registry import get_behaviour_registry


class BehaviourCollection(CollectionBase[Behaviours, Behaviours | BehaviourProtocol], BehaviourCollectionProtocol):
    def get(self, item: Behaviours) -> Optional[BehaviourProtocol]:
        value = super().get(item)

        if isinstance(value, Behaviours):
            behaviour = get_behaviour_registry().get(value)
            self.items[item] = behaviour
            return behaviour

        return value

    def set(self, item: Behaviours) -> None:
        self.items[item] = item

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
        self.load_all()
        return type(self)(self.filter(lambda item: item.can_respond_to(message_type)).items)
