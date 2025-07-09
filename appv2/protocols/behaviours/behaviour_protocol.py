from collections import deque
from typing import runtime_checkable, Protocol, ClassVar, Type

from appv2.behaviours.types import BehaviourAction, MessageHandlersDict
from appv2.config import Behaviours
from appv2.engine.message_broker.types import MessageBody
from appv2.protocols.objects.actor_protocol import ActorProtocol


@runtime_checkable
class BehaviourProtocol(Protocol):
    name: Behaviours
    message_handlers: ClassVar[MessageHandlersDict]
    supported_receivers: ClassVar[tuple[Type[ActorProtocol], ...]]


    @classmethod
    def on_message(cls, receiver: ActorProtocol, message_body: MessageBody) -> deque[BehaviourAction]: ...

    @classmethod
    def can_handle(cls, receiver: ActorProtocol, message_type) -> bool: ...

    @classmethod
    def can_respond_to(cls, message_type) -> bool: ...

    @classmethod
    def register_handlers(cls) -> None: ...
