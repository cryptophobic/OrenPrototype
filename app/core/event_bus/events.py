from enum import Enum, auto

class Events(Enum):
    AnimationUpdate = auto()
    MotionUpdate = auto()
    MousePositionUpdate = auto()
    RegisterCoordinateHolder = auto()
    UnregisterCoordinateHolder = auto()
    RegisterActor = auto()
    UnregisterActor = auto()
