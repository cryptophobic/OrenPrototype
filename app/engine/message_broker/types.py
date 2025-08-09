from collections import UserDict
from dataclasses import dataclass
from enum import Enum

from app.core.types import ContinuousKeyPressEventLogRecords
from app.core.vectors import CustomVec2i, CustomVec2f


class MessageTypes(Enum):
    BUFFERED_MOVE = "buffered_move"
    ANIMATE = "animate"
    INPUT = "input"
    INTENTION_TO_PLACE = "intention_to_place"
    INTENTION_TO_MOVE = "intention_to_move"
    INTENTION_TO_MOVE_DISCRETE = "intention_to_move_discrete"
    INTENTION_TO_STOP = "intention_to_stop"
    KEY_DOWN = "key_down"
    KEY_UP = "key_up"
    OVERLAPPED_BY = "overlapped_by"
    PUSHED_BY = "pushed_by"
    STROKED_BY = "stroked_by"

@dataclass
class Payload:
    pass

@dataclass
class PushedByPayload(Payload):
    force: int
    direction: CustomVec2i

@dataclass
class IntentionToPlacePayload(Payload):
    to_place: CustomVec2i

@dataclass
class SetProperties(Payload):
    properties: dict[str, float|int|str]

@dataclass
class SetVelocityPayload(Payload):
    velocity: CustomVec2f

@dataclass
class StopPayload(Payload):
    direction: CustomVec2i

@dataclass
class MovePayload(Payload):
    direction: CustomVec2i

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

class Controls(UserDict[int, KeyBinding]):
    pass

@dataclass
class InputPayload(Payload):
    actor_name: str
    input: ContinuousKeyPressEventLogRecords

MessagePayloadMap: dict[MessageTypes, type[Payload]] = {
    MessageTypes.BUFFERED_MOVE: AnimatePayload,
    MessageTypes.ANIMATE: AnimatePayload,
    MessageTypes.INPUT: InputPayload,
    MessageTypes.INTENTION_TO_PLACE: IntentionToPlacePayload,
    MessageTypes.INTENTION_TO_MOVE: MovePayload,
    MessageTypes.INTENTION_TO_MOVE_DISCRETE: MovePayload,
    MessageTypes.INTENTION_TO_STOP: StopPayload,
    MessageTypes.OVERLAPPED_BY: Payload,
    MessageTypes.PUSHED_BY: PushedByPayload,
    MessageTypes.STROKED_BY: StrokedByPayload,
}
