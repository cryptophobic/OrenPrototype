from dataclasses import dataclass, field
from typing import Tuple, Dict
from app.config import Behaviours
from appv2.engine.message_broker.types import MessageTypes


@dataclass
class BehaviourAction:
    behaviour: Behaviours
    method_name: str
    args: Tuple = ()
    kwargs: Dict = field(default_factory=dict)

MessageTypeHandlersDict = dict[type, str]
MessageHandlersDict = dict[MessageTypes, tuple[MessageTypeHandlersDict, ...]]
