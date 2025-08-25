from dataclasses import dataclass
from enum import Enum, auto

from arcade import Texture

from app.core.vectors import CustomVec2i, CustomVec2f


class Events(Enum):
    AnimationUpdate = auto()
    MotionUpdate = auto()
    MousePositionUpdate = auto()
    RegisterObject = auto()
    UnregisterObject = auto()

@dataclass
class RegisterObjectPayload

@dataclass
class AnimationUpdatePayload:
    actor_name: str
    animation: list[Texture]

@dataclass
class MotionUpdatePayload:
    actor_name: str
    coordinates: CustomVec2i
    moving_buffer: CustomVec2f

@dataclass
class MousePositionUpdatePayload:
    window_position: CustomVec2i
    world_position: CustomVec2i
    cell_position: CustomVec2i