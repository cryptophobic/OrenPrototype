from collections import deque
from typing import runtime_checkable, Protocol, Optional

from app.behaviours.types import BehaviourAction
from app.engine.message_broker.types import Message
from app.protocols.objects.actor_protocol import ActorProtocol


@runtime_checkable
class MessageBrokerProtocol(Protocol):

    last_message_number: int
    promise_queue: dict[int, deque[BehaviourAction]]
    
    def send_message(self, message: Message, responder: ActorProtocol, no_response: bool = False) -> Optional[int]: ...
    def get_response(self, message_number: int) -> Optional[deque[BehaviourAction]]: ...
