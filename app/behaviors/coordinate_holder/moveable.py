from collections import deque
from typing import Optional, ClassVar

from ..behaviour import Behaviour, BehaviourAction, BehaviourFn
from app.config import Behaviours
from app.bus.message_broker import MessageTypes, Message
from ...objects.actor.actor import Actor

class Moveable(Behaviour):
    name = Behaviours.MOVEABLE
    message_handlers: ClassVar[dict[MessageTypes, deque[BehaviourFn]]] = {}


    @staticmethod
    def pushed_by(receiver: Actor, message: Message) -> Optional[BehaviourAction]:
        # Your real logic here
        return BehaviourAction(behaviour=Behaviours.MOVEABLE, method_name="step_back")

    @classmethod
    def register_handlers(cls):
        cls.message_handlers[MessageTypes.PUSHED_BY] = deque([cls.pushed_by])
