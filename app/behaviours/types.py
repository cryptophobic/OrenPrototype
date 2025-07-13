from dataclasses import dataclass
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, Payload


@dataclass
class BehaviourAction:
    behaviour: Behaviours
    method_name: str
    payload: Payload

MessageTypeHandlersDict = dict[type, str]
MessageHandlersDict = dict[MessageTypes, tuple[MessageTypeHandlersDict, ...]]
