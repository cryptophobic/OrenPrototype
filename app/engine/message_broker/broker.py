from collections import deque
from typing import Optional

from app.behaviours.types import BehaviourAction
from app.engine.message_broker.types import Message
from app.protocols.engine.message_broker.broker_protocol import MessageBrokerProtocol
from app.protocols.objects.actor_protocol import ActorProtocol


class MessageBroker(MessageBrokerProtocol):
    def __init__(self):
        self.last_message_number = 0
        self.promise_queue: dict[int, deque[BehaviourAction]] = {}

    def clear_history(self) -> None:
        self.promise_queue.clear()
        self.last_message_number = 0

    def send_message(self, message: Message, responder: ActorProtocol) -> tuple[int, deque[BehaviourAction]]:
        self.last_message_number += 1
        promise = deque()
        if responder.is_active:
            promise = responder.on_message(message.body)
            message_number = self.last_message_number
            self.promise_queue[message_number] = promise

        return self.last_message_number, promise

    def get_response(self, message_number) -> Optional[deque[BehaviourAction]]:
        return self.promise_queue.pop(message_number, None)
