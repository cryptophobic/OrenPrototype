from dataclasses import dataclass
from enum import Enum
from typing import Deque, Dict, Optional

from app.bus.message_broker.types import Promise
from ..behaviors.behaviour import BehaviourAction
from ..objects.actor.actor import Actor

class MessageBroker:
    def __init__(self):
        self.last_message_number = 0
        self.promise_queue: Dict[int, Promise] = {}

    def send_message(self, message: Message, responder: Actor) -> bool:
        if responder.active:
            promise = responder.on_message(message)
            self.promise_queue[self.last_message_number] = promise
            self.last_message_number += 1
            return True

        return False

    def get_response(self, message_number) -> Optional[Promise]:
        return self.promise_queue.pop(message_number, None)
