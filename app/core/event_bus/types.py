from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

from arcade import Texture

from app.core.types import MapLayer
from app.core.vectors import CustomVec2i, CustomVec2f

class ObjectTypes(Enum):
    INVISIBLE = auto()
    ANIMATED = auto()
    STATIC = auto()

@dataclass(frozen=True)
class RegisterObjectPayload:
    object_name: str
    object_type: ObjectTypes
    coordinates: CustomVec2i
    z_index: MapLayer = MapLayer.OBJECTS
    icon_path: Path = field(default_factory=Path)
    animations: list[Texture] = field(default_factory=list)

@dataclass(frozen=True)
class ObjectPayload:
    object_name: str

@dataclass(frozen=True)
class ObjectPositionPayload:
    object_name: str
    coordinates: CustomVec2i

@dataclass(frozen=True)
class SpriteAnimationUpdatePayload:
    object_name: str
    animation: list[Texture]

@dataclass(frozen=True)
class ShapeAnimationUpdatePayload:
    animation: list[Texture]

@dataclass(frozen=True)
class MotionUpdatePayload:
    object_name: str
    coordinates: CustomVec2i
    moving_buffer: CustomVec2f

@dataclass(frozen=True)
class MousePositionUpdatePayload:
    window_position: CustomVec2i
    world_position: CustomVec2i
    cell_position: CustomVec2i