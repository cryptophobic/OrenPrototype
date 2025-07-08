from typing import Self, Optional

from appv2.engine.message_broker.types import MessageTypes
from appv2.config import Behaviours
from appv2.core.collection_base import CollectionBase
from appv2.protocols.behaviour_protocol import BehaviourProtocol
from appv2.registry.behaviour_registry import get_registry


class BehaviourCollection(CollectionBase[Behaviours, Behaviours | BehaviourProtocol]):
    def __init__(self, items: dict[Behaviours, Behaviours | BehaviourProtocol] | None = None):
        super().__init__(items or {})

    def __getitem__(self, item: Behaviours) -> Optional[BehaviourProtocol]:
        value = self.data.get(item)

        if isinstance(value, Behaviours):
            behaviour = get_registry().get(value)
            self.data[item] = behaviour
            return behaviour

        return value

    def can_respond_to(self, message_type: MessageTypes) -> Self:
        return type(self)(
            self.filter(
                lambda a: (
                    get_registry().get(a).can_respond_to(message_type)
                    if isinstance(a, Behaviours)
                    else a.can_respond_to(message_type)
                )
            )
        )
