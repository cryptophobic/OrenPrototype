from collections import deque
from typing import ClassVar, Iterable

from app.behaviours.logic.movement_utils import MovementUtils
from app.behaviours.types import MessageTypeHandlersDict, BehaviourAction, HandlersMap
from app.core.event_bus.bus import EventBus
from app.protocols.engine.grid.grid_protocol import GridProtocol
from app.protocols.engine.message_broker.broker_protocol import MessageBrokerProtocol
from app.protocols.objects.actor_protocol import ActorProtocol
from app.engine.message_broker.types import MessageTypes, MessageBody, MessagePayloadMap
from app.config import Behaviours


def handles(message: MessageTypes, for_: Iterable[type] | type):
    """Mark a method as a handler for one message; works inside the class."""
    if isinstance(for_, type):
        receiver_types: tuple[type, ...] = (for_,)
    else:
        receiver_types = tuple(for_)

    def deco(func):
        specs = getattr(func, "_handler_specs", [])
        specs.append((message, receiver_types))
        setattr(func, "_handler_specs", specs)
        return func
    return deco

# Base Behaviour class
class Behaviour:
    _movement_utils = None
    name: ClassVar[Behaviours] = Behaviours.BEHAVIOUR
    message_handlers: ClassVar[HandlersMap] = {}
    supported_receivers = (ActorProtocol,)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.message_handlers = {}

        # scan class dict for methods tagged by @handles
        for attr_name, member in cls.__dict__.items():
            func = getattr(member, "__func__", member)  # in case it's a @classmethod
            specs = getattr(func, "_handler_specs", None)
            if not specs:
                continue

            for message_type, receiver_types in specs:
                lst = cls.message_handlers.setdefault(message_type, [])
                for rt in receiver_types:
                    lst.append({rt: attr_name})


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

        # TODO: Debug why method_names are incorrect
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
    def on_message(cls, receiver: ActorProtocol, message_body: MessageBody) -> deque:
        resp = deque()
        if message_body.message_type in cls.message_handlers and isinstance(receiver, cls.supported_receivers):
            for handler in cls.message_handlers[message_body.message_type]:
                resp.extend(cls.route_to_receiver_method(receiver, handler, message_body))
        return resp

    @classmethod
    def can_handle(cls, receiver: ActorProtocol, message_type: MessageTypes) -> bool:
        return isinstance(receiver, cls.supported_receivers) and cls.can_respond_to(message_type)

    @classmethod
    def can_respond_to(cls, message_type: MessageTypes) -> bool:
        return message_type in cls.message_handlers


    @classmethod
    def register_event_bus(cls, event_bus: EventBus):
        cls._event_bus = event_bus

    @classmethod
    def get_event_bus(cls) -> EventBus:
        if cls._event_bus is None:
            raise RuntimeError("Event bus is not registered in Behaviour.")

        return cls._event_bus


    @classmethod
    def register_messenger(cls, broker: MessageBrokerProtocol):
        cls._messenger = broker

    @classmethod
    def get_messenger(cls) -> MessageBrokerProtocol:
        if cls._messenger is None:
            raise RuntimeError("MessageBroker is not registered in Behaviour.")

        return cls._messenger


    @classmethod
    def register_grid(cls, grid: GridProtocol):
        cls._grid = grid

    @classmethod
    def get_grid(cls) -> GridProtocol:
        if cls._grid is None:
            raise RuntimeError("Grid is not registered in Behaviour.")

        return cls._grid


    @classmethod
    def get_movement_utils(cls) -> MovementUtils:
        if cls._movement_utils is None:
            cls._movement_utils = MovementUtils(cls.get_grid(), cls.get_messenger())

        return cls._movement_utils

    @classmethod
    def register_handlers(cls):
        pass
