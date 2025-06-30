from typing import Dict, Optional

from .types import Promise, Message
from ...objects.actor.actor import Actor

class MessageBroker:
    def __init__(self):
        self.last_message_number = 0
        self.promise_queue: Dict[int, Promise] = {}

    def send_message(self, message: Message, responder: Actor) -> Optional[int]:
        if responder.active:
            promise = responder.on_message(message)
            message_number = self.last_message_number
            self.promise_queue[message_number] = promise
            self.last_message_number += 1
            return message_number

        return None

    def get_response(self, message_number) -> Optional[Promise]:
        return self.promise_queue.pop(message_number, None)
