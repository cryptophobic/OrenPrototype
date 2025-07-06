from typing import Dict, Optional, Deque

from .types import Message
from ...behaviors.types import BehaviourAction
from ...objects.actor.actor import Actor

class MessageBroker:
    def __init__(self):
        self.last_message_number = 0
        self.promise_queue: Dict[int, Deque[BehaviourAction]] = {}

    def send_message(self, message: Message, responder: Actor, no_response: bool=False) -> Optional[int]:
        if responder.active:
            promise = responder.on_message(message.body)
            print(promise.reason)
            if not no_response:
                message_number = self.last_message_number
                self.promise_queue[message_number] = promise
                self.last_message_number += 1
                return message_number

        return None

    def get_response(self, message_number) -> Optional[Deque[BehaviourAction]]:
        return self.promise_queue.pop(message_number, None)
