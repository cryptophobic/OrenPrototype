from dataclasses import dataclass
from typing import Any

from app.config import Behaviours
from app.core.vectors import CustomVec2f
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
    moving_buffer: CustomVec2f
    aggregated_delta: float = 0.0
    threshold: float = 0.1

