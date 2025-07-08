from typing import Self

from appv2.engine.message_broker.types import MessageTypes
from appv2.config import Behaviours
from appv2.core.collection_base import CollectionBase
from appv2.protocols.behaviour_protocol import BehaviourProtocol


class BehavioursCollection(CollectionBase[Behaviours, BehaviourProtocol]):
    def __init__(self, items: dict[Behaviours, BehaviourProtocol] | None = None):
        super().__init__(items or {})

    def can_response_to(self, message_type: MessageTypes) -> Self:
        return type(self)(self.filter(lambda a: a.can_handle(message_type)))
