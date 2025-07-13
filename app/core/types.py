from collections import namedtuple, deque

KeyPressEventLogRecord = namedtuple("KeyPressEventLogRecord", ["dt", "key", "down", "subscribers_set"])
KeyPressEventLogRecords = deque[KeyPressEventLogRecord]