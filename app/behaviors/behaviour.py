from typing import Callable, ClassVar, Optional
from app.bus.message_broker import MessageTypes
from app.config import Behaviours
from app.objects.actor.actor import Actor

# A behaviour function always returns True if it handled the message
BehaviourFn = Callable[..., bool]


class Behaviour:
    name: ClassVar[Behaviours] = Behaviours.BEHAVIOUR
    message_handlers: ClassVar[dict[MessageTypes, BehaviourFn]] = {}

    @staticmethod
    def on_message(message_type: MessageTypes) -> Optional[BehaviourFn]:
        if Behaviour.can_respond_to(message_type):
            return Behaviour.message_handlers[message_type]

        return None

    @classmethod
    def can_respond_to(cls, message_type: MessageTypes) -> bool:
        return message_type in cls.message_handlers

