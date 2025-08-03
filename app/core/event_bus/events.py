from dataclasses import dataclass
from enum import Enum, auto


class Events(Enum):
    AnimationUpdate = auto()

@dataclass
class AnimationUpdatePayload:
    actor_name: str