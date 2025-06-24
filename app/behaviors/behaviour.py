from collections import deque
from dataclasses import dataclass, field
from typing import Callable, ClassVar
from ..bus.message_broker import MessageTypes, Message
from ..config import Behaviours
from ..objects.actor.actor import Actor


@dataclass
class BehaviourAction:
    behaviour: Behaviours
    method_name: str
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)

BehaviourFn = Callable[[Actor, Message], BehaviourAction]

# Base Behaviour class
class Behaviour:
    name: ClassVar[Behaviours] = Behaviours.BEHAVIOUR
    message_handlers: ClassVar[dict[MessageTypes, deque[BehaviourFn]]] = {}

    @classmethod
    def on_message(cls, actor: Actor, message: Message) -> deque[BehaviourAction]:
        response_actions: deque[BehaviourAction] = deque()
        if cls.can_respond_to(message.message_type):
            for handler in cls.message_handlers[message.message_type]:
                action = handler(actor, message)
                if action:
                    response_actions.append(action)

        return response_actions

    @classmethod
    def can_respond_to(cls, message_type: MessageTypes) -> bool:
        return message_type in cls.message_handlers

