from collections import namedtuple, deque

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