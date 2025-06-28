from collections import deque
from typing import Optional, ClassVar

from ..behaviour import Behaviour, BehaviourAction, BehaviourFn
from app.config import Behaviours
from app.bus.message_broker import MessageTypes, Message
from ...objects.actor.actor import Actor

class Moveable(Behaviour):
    name = Behaviours.MOVEABLE
    message_handlers: ClassVar[dict[MessageTypes, deque[BehaviourFn]]] = {}


    @classmethod
    def pushed_by(cls, receiver: Actor, message: Message) -> Optional[BehaviourAction]:
        # Your real logic here
        return BehaviourAction(behaviour=Behaviours.MOVEABLE, method_name="step_back", args=(receiver, message))

    def step_back(self, actor: Actor, message: Message):

    @classmethod
    def register_handlers(cls):
        cls.message_handlers[MessageTypes.PUSHED_BY] = deque([cls.pushed_by])
