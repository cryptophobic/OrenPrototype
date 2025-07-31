from collections import UserDict
from dataclasses import dataclass
from enum import Enum

from app.core.types import KeyPressEventLogRecords
from app.core.vectors import CustomVec2i, CustomVec2f


class MessageTypes(Enum):
    BUFFERED_MOVE = "buffered_move"
    ANIMATE = "animate"
    INPUT = "input"
    INTENTION_TO_MOVE = "intention_to_move"
    KEY_DOWN = "key_down"
    KEY_UP = "key_up"
    OVERLAPPED_BY = "overlapped_by"
    PUSHED_BY = "pushed_by"
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
    direction: CustomVec2i

@dataclass
class IntentionToMovePayload(Payload):
    direction: CustomVec2i

@dataclass
class SetVelocityPayload(Payload):
    velocity: CustomVec2f

@dataclass
class AnimatePayload(Payload):
    delta_time: float

@dataclass
class StrokedByPayload(Payload):
    damage: int
    damage_type: str
    direction: CustomVec2i

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
    repeat_delta: int = -1
    key_up: MessageBody = None

@dataclass
class InputPayload(Payload):
    input: KeyPressEventLogRecords

class Controls(UserDict[int, KeyBinding]):
    pass

MessagePayloadMap: dict[MessageTypes, type[Payload]] = {
    MessageTypes.BUFFERED_MOVE: AnimatePayload,
    MessageTypes.ANIMATE: AnimatePayload,
    MessageTypes.INPUT: InputPayload,
    MessageTypes.INTENTION_TO_MOVE: IntentionToMovePayload,
    MessageTypes.KEY_DOWN: ControlsPayload,
    MessageTypes.KEY_UP: ControlsPayload,
    MessageTypes.OVERLAPPED_BY: Payload,
    MessageTypes.PUSHED_BY: PushedByPayload,
    MessageTypes.STROKED_BY: StrokedByPayload,
}
