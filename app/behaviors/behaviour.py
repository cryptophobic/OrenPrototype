from collections import deque
from dataclasses import dataclass, field
from typing import Callable, ClassVar
from ..bus.message_broker.types import MessageTypes, MessageBody
from ..config import Behaviours
from ..context.context import Context
from ..objects.actor.actor import Actor


@dataclass
class BehaviourAction:
    behaviour: Behaviours
    method_name: str
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)

BehaviourFn = Callable[[Actor, MessageBody], BehaviourAction]

# Base Behaviour class
class Behaviour:
    name: ClassVar[Behaviours] = Behaviours.BEHAVIOUR
    message_handlers: ClassVar[dict[MessageTypes, tuple[BehaviourFn, ...]]] = {}
    supported_receivers = (Actor,)
    context = Context.instance()

    @classmethod
    def on_message(cls, receiver: Actor, message_body: MessageBody) -> deque[BehaviourAction]:
        response_actions: deque[BehaviourAction] = deque()
        if cls.can_handle(receiver, message_body.message_type):
            for handler in cls.message_handlers[message_body.message_type]:
                action = handler(receiver, message_body)
                if action:
                    response_actions.append(action)

        return response_actions

    @classmethod
    def can_handle(cls, receiver: Actor, message_type: MessageTypes) -> bool:
        return (
                isinstance(receiver, cls.supported_receivers)
                and message_type in cls.message_handlers
        )

    @classmethod
    def register_handlers(cls):
        pass

