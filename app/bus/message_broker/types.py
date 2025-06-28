from dataclasses import dataclass
from enum import Enum
from typing import Deque

from app.behaviors.behaviour import BehaviourAction
from app.objects.actor.actor import Actor


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

