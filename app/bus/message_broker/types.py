from dataclasses import dataclass
from enum import Enum
from typing import Deque

from ...behaviors.behaviour import BehaviourAction
from ...helpers.vectors import Vec2

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...objects.actor.actor import Actor


@dataclass
class Promise:
    responder: Actor
    response_actions: Deque[BehaviourAction]
    reason: str # possible debug

class MessageTypes(Enum):
    KEY_DOWN = "key_down"
    KEY_UP = "key_up"
    PUSHED_BY = "pushed_by"
    OVERLAPPED_BY = "overlapped_by"
    STROKED_BY = "stroked_by"

@dataclass
class Payload:
    pass

@dataclass
class ControlsPayload(Payload):
    key_code: int

@dataclass
class PushedByPayload(Payload):
    force: int
    direction: Vec2

@dataclass
class StrokedByPayload(Payload):
    damage: int
    damage_type: str
    direction: Vec2

@dataclass
class MessageBody:
    message_type: MessageTypes
    payload: Payload

@dataclass
class Message:
    sender: Actor
    body: MessageBody
