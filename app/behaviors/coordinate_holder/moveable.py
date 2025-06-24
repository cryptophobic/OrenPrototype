# app/behaviors/coordinate_holder/moveable.py

from ..behaviour import Behaviour
from app.config import Behaviours
from app.bus.message_broker import MessageTypes, Message
from ...objects.actor.actor import Actor

class Moveable(Behaviour):
    name = Behaviours.MOVEABLE


    @staticmethod
    def pushed_by(receiver: Actor, message: Message) -> bool:
        # Basic sample logic: log it and mark receiver as dirty
        print(f"{receiver.name} was pushed by {message.sender.name}")
        receiver.body.velocity += message.sender.body.velocity
        receiver.dirty = True
        return True

    message_handlers = {
        MessageTypes.PUSHED_BY: pushed_by,
    }
