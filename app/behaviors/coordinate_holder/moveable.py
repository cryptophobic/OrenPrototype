from collections import deque
from typing import Optional, ClassVar

from ..behaviour import Behaviour, BehaviourAction, BehaviourFn
from app.config import Behaviours
from ...bus.message_broker.types import MessageTypes, Message, PushedByPayload
from ...objects.actor.actor import Actor

class Moveable(Behaviour):
    name = Behaviours.MOVEABLE
    message_handlers: ClassVar[dict[MessageTypes, deque[BehaviourFn]]] = {}

    @staticmethod
    def pushed_by(receiver: Actor, message: Message) -> Optional[BehaviourAction]:
        if isinstance(message.payload, PushedByPayload):
            pushed_payload = message.payload
            
            if pushed_payload.force > 10:
                return BehaviourAction(
                    behaviour=Behaviours.MOVEABLE, 
                    method_name="knockback",
                    kwargs={"direction": pushed_payload.direction, "distance": pushed_payload.force // 5}
                )
            else:
                return BehaviourAction(
                    behaviour=Behaviours.MOVEABLE, 
                    method_name="step_back",
                    kwargs={"direction": pushed_payload.direction}
                )
        
        return BehaviourAction(behaviour=Behaviours.MOVEABLE, method_name="step_back")

    @classmethod
    def register_handlers(cls):
        cls.message_handlers[MessageTypes.PUSHED_BY] = deque([cls.pushed_by])
