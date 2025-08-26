from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

from arcade import Texture

from app.core.types import MapLayer
from app.core.vectors import CustomVec2i, CustomVec2f

class ObjectTypes(Enum):
    ANIMATED = auto()
    STATIC = auto()

class Events(Enum):
    AnimationUpdate = auto()
    MotionUpdate = auto()
    MousePositionUpdate = auto()
    RegisterObject = auto()
    UnregisterObject = auto()

@dataclass(frozen=True)
class UnregisterObjectPayload:
    object_name: str

@dataclass(frozen=True)
class RegisterObjectPayload:
    object_name: str
    object_type: ObjectTypes
    z_index: MapLayer = MapLayer.OBJECTS
    icon_path: Path = field(default_factory=Path)
    animations: list[Texture] = field(default_factory=list)

@dataclass(frozen=True)
class AnimationUpdatePayload:
    actor_name: str
    animation: list[Texture]

@dataclass(frozen=True)
class MotionUpdatePayload:
    actor_name: str
    coordinates: CustomVec2i
    moving_buffer: CustomVec2f

@dataclass(frozen=True)
class MousePositionUpdatePayload:
    window_position: CustomVec2i
    world_position: CustomVec2i
    cell_position: CustomVec2i