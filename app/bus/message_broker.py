from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Deque, Dict

from ..objects.actor.actor import Actor
from .command_pipeline import ActorAction

@dataclass
class Promise:
    responder: Actor
    response_actions: Deque[ActorAction]
    reason: str

class Reasons(Enum):
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
    reason: Reasons
    payload: Payload

class MessageBroker:
    def __init__(self):
        self.promise_queue: Dict[str, Deque[Promise]] = {}

    def send_message(self, message: Message, responder: Actor) -> bool:
        if responder.active:
            # Actor.on_message is obliged to return Promise.
            # With empty response_actions at least.
            promise = responder.on_message(message)
            self.promise_queue.setdefault(message.sender.name, deque()).append(promise)
            return True

        return False

    def get_response(self, sender: Actor) -> Deque[Promise]:
        return self.promise_queue.pop(sender.name, deque())
