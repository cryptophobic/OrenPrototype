from dataclasses import dataclass
from enum import Enum, auto

from app.core.vectors import CustomVec2i


class Events(Enum):
    AnimationUpdate = auto()
    MousePositionUpdate = auto()

@dataclass
class AnimationUpdatePayload:
    actor_name: str


@dataclass
class MousePositionUpdatePayload:
    window_position: CustomVec2i
    world_position: CustomVec2i
    cell_position: CustomVec2i