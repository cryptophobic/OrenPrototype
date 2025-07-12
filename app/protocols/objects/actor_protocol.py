from collections import deque
from typing import Protocol, List, runtime_checkable, Self
from app.engine.message_broker.types import MessageBody
from app.behaviours.types import BehaviourAction
from app.config import Behaviours


@runtime_checkable
class ActorProtocol(Protocol):
    name: str
    is_active: bool
    is_deleted: bool
    pending_actions: deque[BehaviourAction]

    def on_message(self, message_body: MessageBody) -> deque[BehaviourAction]: ...
    def is_behave_as_this(self, behaviour: Behaviours) -> bool: ...
    def is_behave_as_them(self, behaviours: List[Behaviours]) -> bool: ...
    def add_behaviour_from_enum(self, behaviour: Behaviours) -> Self: ...
    def remove_behaviour_from_enum(self, behaviour: Behaviours) -> Self: ...
