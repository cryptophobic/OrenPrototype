from dataclasses import dataclass
from typing import Any

from app.config import Behaviours
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
