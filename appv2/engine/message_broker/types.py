from collections import UserDict
from dataclasses import dataclass
from enum import Enum

from appv2.core.vectors import Vec2


class MessageTypes(Enum):
    KEY_DOWN = "key_down"
    KEY_UP = "key_up"
    PUSHED_BY = "pushed_by"
    OVERLAPPED_BY = "overlapped_by"
    STROKED_BY = "stroked_by"
    INTENTION_TO_MOVE = "intention_to_move"

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
class IntentionToMovePayload(Payload):
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
    sender: str
    body: MessageBody

@dataclass
class KeyBinding:
    key_down: MessageBody
    key_up: MessageBody = None

class Controls(UserDict[int, KeyBinding]):
    pass

MessagePayloadMap: dict[MessageTypes, type[Payload]] = {
    MessageTypes.KEY_DOWN: ControlsPayload,
    MessageTypes.KEY_UP: ControlsPayload,
    MessageTypes.PUSHED_BY: PushedByPayload,
    MessageTypes.OVERLAPPED_BY: Payload,
    MessageTypes.STROKED_BY: StrokedByPayload,
    MessageTypes.INTENTION_TO_MOVE: IntentionToMovePayload,
}
