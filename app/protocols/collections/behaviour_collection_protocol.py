from typing import Protocol, Self, runtime_checkable
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes
from app.protocols.behaviours.behaviour_protocol import BehaviourProtocol

@runtime_checkable
class BehaviourCollectionProtocol(Protocol):
    def get(self, item: Behaviours) -> BehaviourProtocol | None: ...
    def load_all(self) -> None: ...
    def can_respond_to(self, message_type: MessageTypes) -> Self: ...
