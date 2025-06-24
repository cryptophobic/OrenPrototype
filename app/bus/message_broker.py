from dataclasses import dataclass
from enum import Enum
from typing import Deque, Dict, Optional

from ..behaviors.behaviour import BehaviourAction
from ..objects.actor.actor import Actor

@dataclass
class Promise:
    responder: Actor
    response_actions: Deque[BehaviourAction]
    reason: str # possible debug

class MessageTypes(Enum):
    PUSHED_BY = "pushed_by"
    STROKED_BY = "stroked_by"

@dataclass
class Payload:
    # TODO: expand later to store possible details.
    # e.g. direction of pushing, striking
    # parameters of strike (magic, physical, fire, power of strike etc)
    pass

@dataclass
class Message:
    sender: Actor
    message_type: MessageTypes
    payload: Payload

class MessageBroker:
    def __init__(self):
        self.last_message_number = 0
        self.promise_queue: Dict[int, Promise] = {}

    def send_message(self, message: Message, responder: Actor) -> bool:
        if responder.active:
            # Actor.on_message is obliged to return Promise.
            # With empty response_actions at least.
            promise = responder.on_message(message)
            self.promise_queue[self.last_message_number] = promise
            self.last_message_number += 1
            return True

        return False

    def get_response(self, message_number) -> Optional[Promise]:
        return self.promise_queue.pop(message_number, None)
