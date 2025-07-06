from dataclasses import dataclass, field
from typing import Tuple, Dict
from app.config import Behaviours

@dataclass
class BehaviourAction:
    behaviour: Behaviours
    method_name: str
    args: Tuple = ()
    kwargs: Dict = field(default_factory=dict)
