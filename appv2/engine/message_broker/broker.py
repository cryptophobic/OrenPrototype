from collections import deque
from typing import Optional

from appv2.behaviours.types import BehaviourAction
from appv2.engine.message_broker.types import Message
from appv2.protocols.objects.actor_protocol import ActorProtocol


class MessageBroker:
    def __init__(self):
        self.last_message_number = 0
        self.promise_queue: dict[int, deque[BehaviourAction]] = {}

    def send_message(self, message: Message, responder: ActorProtocol, no_response: bool=False) -> Optional[int]:
        if responder.active:
            promise = responder.on_message(message.body)
            if not no_response:
                message_number = self.last_message_number
                self.promise_queue[message_number] = promise
                self.last_message_number += 1
                return message_number

        return None

    def get_response(self, message_number) -> Optional[deque[BehaviourAction]]:
        return self.promise_queue.pop(message_number, None)
