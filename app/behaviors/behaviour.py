from typing import Callable, ClassVar
from app.bus.message_broker import MessageTypes
from app.config import Behaviours

# A behaviour function always returns True if it handled the message
BehaviourFn = Callable[..., bool]


class Behaviour:
    name: ClassVar[Behaviours] = Behaviours.GENERAL
    message_handlers: ClassVar[dict[MessageTypes, BehaviourFn]] = {}

    @classmethod
    def can_respond_to(cls, message_type: MessageTypes) -> bool:
        return message_type in cls.message_handlers

