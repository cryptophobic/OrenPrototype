from dataclasses import dataclass, field
from typing import NamedTuple

from app.config import Behaviours
from app.core.vectors import CustomVec2f, CustomVec2i
from app.engine.message_broker.types import MessageTypes, Payload


@dataclass
class BehaviourAction:
    behaviour: Behaviours
    method_name: str
    payload: Payload

@dataclass(frozen=True, slots=True)
class BehaviourState:
    pass

MessageTypeHandlersDict = dict[type, str]
MessageHandlersDict = dict[MessageTypes, tuple[MessageTypeHandlersDict, ...]]
BehaviourStates = dict[Behaviours, BehaviourState]

ReceiverMap = dict[type, str] # {ReceiverType: "method_name"}
HandlersMap = dict[MessageTypes, list[ReceiverMap]]

SimpleVec2Bool = NamedTuple("SimpleVec2", x=bool, y=bool)

@dataclass(frozen=True, slots=True)
class BufferedMoverState(BehaviourState):
    moving_buffer: CustomVec2f = CustomVec2f(0, 0)
    intent_velocity: CustomVec2f = CustomVec2i(0, 0)
    intent_velocity_normalised: CustomVec2f = CustomVec2f(0, 0)
    clear_velocity: SimpleVec2Bool = SimpleVec2Bool(False, False)

