from enum import Enum, auto

class Events(Enum):
    AnimationUpdate = auto()
    MotionUpdate = auto()
    MousePositionUpdate = auto()
    RegisterCoordinateHolder = auto()
    MoveCoordinateHolder = auto()
    UnregisterCoordinateHolder = auto()
    RegisterActor = auto()
    UnregisterActor = auto()
