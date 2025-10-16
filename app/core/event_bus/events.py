from enum import Enum, auto

class Events(Enum):
    ShapeAnimationUpdate = auto()
    SpriteAnimationUpdate = auto()
    MotionUpdate = auto()
    MousePositionUpdate = auto()
    RegisterSprite = auto()
    MoveCoordinateHolder = auto()
    UnregisterSprite = auto()
    RegisterActor = auto()
    UnregisterActor = auto()
