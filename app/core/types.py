from collections import namedtuple, deque
from enum import IntEnum

KeyPressEventLogRecord = namedtuple(
    "KeyPressEventLogRecord",
    ["dt", "key", "down", "subscribers_set"]
)
KeyPressEventLogRecords = deque[KeyPressEventLogRecord]

ContinuousKeyPressEventLogRecord = namedtuple(
    "ContinuousKeyPressEventLogRecord",
    ["dt", "key", "down"]
)
ContinuousKeyPressEventLogRecords = list[ContinuousKeyPressEventLogRecord]

class Layer(IntEnum):
    GROUND          = 0
    MATERIAL        = 1
    OBJECTS         = 2
    BIG_OBJECTS     = 3
    FLYING_1        = 4
    FLYING_2        = 5
    FOG_OF_WAR      = 6
    UI_OVERLAY      = 7

NUM_LAYERS = max(Layer) + 1
