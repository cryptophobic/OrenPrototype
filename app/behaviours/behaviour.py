from collections import deque
from typing import Callable, ClassVar, TYPE_CHECKING

from .types import BehaviourAction
from ..bus.message_broker.types import MessageTypes, MessageBody, MessagePayloadMap
from ..config import Behaviours
from ..context.context import Context
from ..protocols.actor_protocol import ActorProtocol

if TYPE_CHECKING:
    from ..objects.actor.actor import Actor

BehaviourFn = Callable[[ActorProtocol, MessageBody], deque[BehaviourAction]]
MessageTypeHandlersDict = dict[type, str]
MessageHandlersDict = dict[MessageTypes, tuple[MessageTypeHandlersDict, ...]]

def register_message_handler(message_type: MessageTypes, handlers: dict[type, str]):
    def decorator(cls: type[Behaviour]):
        existing = cls.message_handlers.get(message_type, ())
        cls.message_handlers[message_type] = existing + (handlers,)
        return cls

    return decorator

# Base Behaviour class
class Behaviour:
    name: ClassVar[Behaviours] = Behaviours.BEHAVIOUR
    message_handlers: ClassVar[MessageHandlersDict] = {}
    supported_receivers = (ActorProtocol,)
    context = Context.instance()

    @classmethod
    def route_to_receiver_method(
            cls,
            receiver: ActorProtocol,
            handlers_ref: MessageTypeHandlersDict,
            message_body: MessageBody,
    ) -> deque[BehaviourAction]:
        expected_payload_type = MessagePayloadMap.get(message_body.message_type)
        if expected_payload_type and not isinstance(message_body.payload, expected_payload_type):
            raise TypeError(f"Expected {expected_payload_type.__name__}, got {type(message_body.payload).__name__}")

        for receiver_type, method_name in handlers_ref.items():
            if isinstance(receiver, receiver_type):
                return deque([
                    BehaviourAction(
                        behaviour=cls.name,
                        method_name=method_name,
                        kwargs=message_body.payload.__dict__,
                    )
                ])
        return deque()

    @classmethod
    def on_message(cls, receiver: ActorProtocol, message_body: MessageBody) -> deque[BehaviourAction]:
        response_actions: deque[BehaviourAction] = deque()
        if cls.can_handle(receiver, message_body.message_type):
            for handler in cls.message_handlers[message_body.message_type]:
                response_actions.extend(cls.route_to_receiver_method(receiver, handler, message_body))

        return response_actions

    @classmethod
    def can_handle(cls, receiver: ActorProtocol, message_type: MessageTypes) -> bool:
        return (
                isinstance(receiver, cls.supported_receivers)
                and message_type in cls.message_handlers
        )

    @classmethod
    def register_handlers(cls):
        pass
