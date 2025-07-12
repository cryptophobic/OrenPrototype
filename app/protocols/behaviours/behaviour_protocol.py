from collections import deque
from typing import runtime_checkable, Protocol, ClassVar, Type

from app.behaviours.types import BehaviourAction, MessageHandlersDict
from app.config import Behaviours
from app.engine.message_broker.types import MessageBody
from app.protocols.engine.grid.grid_protocol import GridProtocol
from app.protocols.engine.message_broker.broker_protocol import MessageBrokerProtocol
from app.protocols.objects.actor_protocol import ActorProtocol


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

    @classmethod
    def register_messenger(cls, broker: MessageBrokerProtocol): ...

    @classmethod
    def get_messenger(cls) -> MessageBrokerProtocol: ...

    @classmethod
    def register_grid(cls, broker: GridProtocol): ...

    @classmethod
    def get_grid(cls) -> GridProtocol: ...

