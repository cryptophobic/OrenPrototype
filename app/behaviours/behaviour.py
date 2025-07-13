from collections import deque
from typing import ClassVar

from app.behaviours.types import MessageHandlersDict, MessageTypeHandlersDict, BehaviourAction
from app.protocols.engine.grid.grid_protocol import GridProtocol
from app.protocols.engine.message_broker.broker_protocol import MessageBrokerProtocol
from app.protocols.objects.actor_protocol import ActorProtocol
from app.engine.message_broker.types import MessageTypes, MessageBody, MessagePayloadMap
from app.config import Behaviours


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
                        payload=message_body.payload,
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
                and cls.can_respond_to(message_type)
        )

    @classmethod
    def can_respond_to(cls, message_type: MessageTypes) -> bool:
        return (
                message_type in cls.message_handlers
        )

    @classmethod
    def register_messenger(cls, broker: MessageBrokerProtocol):
        cls._messenger = broker

    @classmethod
    def get_messenger(cls) -> MessageBrokerProtocol:
        if cls._messenger is None:
            raise RuntimeError("MessageBroker not registered in Behaviour.")
        return cls._messenger

    @classmethod
    def register_grid(cls, grid: GridProtocol):
        cls._grid = grid

    @classmethod
    def get_grid(cls) -> GridProtocol:
        if cls._grid is None:
            raise RuntimeError("Grid not registered in Behaviour.")
        return cls._grid

    @classmethod
    def register_handlers(cls):
        pass
