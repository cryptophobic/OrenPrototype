from dataclasses import dataclass


@dataclass
class KeyPressLogRecord:
    dt: int
    down: bool
    processed: bool = False


@dataclass
class KeyPressLog:
    down: bool
    interval: int
    log: list[KeyPressLogRecord]
    subscribers: int
    subscribers_set: set[str]


class InputEventsContinuous:
    def __init__(self):
        self.subscribers: dict[str, tuple[int, ...]] = {}
        self.key_map: dict[int, KeyPressLog] = {}

