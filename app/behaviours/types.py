from dataclasses import dataclass, field
from typing import Any

from app.config import Behaviours
from app.core.vectors import CustomVec2f, CustomVec2i
from app.engine.message_broker.types import MessageTypes, Payload


@dataclass
class BehaviourAction:
    behaviour: Behaviours
    method_name: str
    payload: Payload

@dataclass
class BehaviourState:
    pass

MessageTypeHandlersDict = dict[type, str]
MessageHandlersDict = dict[MessageTypes, tuple[MessageTypeHandlersDict, ...]]
BehaviourStates = dict[Behaviours, BehaviourState]


@dataclass
class BufferedMoverState(BehaviourState):
    moving_buffer: CustomVec2f = field(default_factory=lambda: CustomVec2f(0, 0))
    intent_velocity: CustomVec2f = field(default_factory=lambda: CustomVec2f(0, 0))
    clear_velocity: CustomVec2i = field(default_factory=lambda: CustomVec2i(0, 0))
    aggregated_delta: float = 0.0
    threshold: float = 0.1

