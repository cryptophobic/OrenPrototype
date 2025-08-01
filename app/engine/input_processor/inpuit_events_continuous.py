from collections import namedtuple
from dataclasses import dataclass

from app.engine.message_broker.types import Controls


@dataclass
class KeyPressLogRecord:
    dt: int
    down: bool
    processed: bool = False


@dataclass
class KeyPressLog:
    down: bool
    interval: int
    subscriber: str
    log: list[KeyPressLogRecord]
    updated: int = 0

@dataclass
class KeysUpDownState:
    down: dict[int, int]
    up: dict[int, int]

class InputEventsContinuous:
    flushing_interval = 10000

    def __init__(self, ticks: int = 0):
        self.subscribers: dict[str, tuple[int, ...]] = {}
        self.key_map: dict[int, KeyPressLog] = {}
        self.ticks = ticks
        self.next_flush = self.ticks + self.flushing_interval

        self.key_pressed: set[int] = set()


    def subscribe(self, subscriber_name: str, keys: Controls):
        for key, binding in keys.items():
            if self.key_map.get(key) is None:
                self.key_map[key] = KeyPressLog(
                    down=False,
                    interval=binding.repeat_delta,
                    subscriber=subscriber_name,
                    log=[],
                )

        self.subscribers[subscriber_name] = tuple(k for k in keys.keys())
        return True

    def unsubscribe(self, subscriber: str):
        if subscriber not in self.subscribers:
            return False

        for key in self.subscribers[subscriber]:
            if key not in self.key_map:
                continue

            del self.key_map[key]

        del self.subscribers[subscriber]

        return True

    def flush(self):
        if self.ticks > self.next_flush:
            frame = max(0, self.next_flush - self.flushing_interval)
            for value in self.key_map.values():
                value.log = [log for log in value.log if log.dt >= frame]

            self.next_flush = self.ticks + self.flushing_interval

    def register_key_pressed(self, key: int, pressed: bool):
        if not pressed:
            self.key_pressed.discard(key)
        elif not key in self.key_map:
            return
        else:
            self.key_pressed.add(key)

    def is_key_registered(self, key: int) -> bool:
        return key in self.key_map

    def is_down_event_expired(self, key: int) -> bool:
        if not self.is_key_registered(key):
            return False

        key_map = self.key_map.get(key)
        if not key_map.down or key_map.interval < 0:
            return False

        if key_map.updated <= self.ticks - key_map.interval:
            return True

        return False

    def listen(self, ticks: int):
        self.ticks = ticks
        pressed = self.key_pressed

        for key in pressed:
            if not self.is_key_registered(key):
                continue

            key_map = self.key_map.get(key)

            if key_map.down:
                is_key_down = not self.is_down_event_expired(key)
            else:
                is_key_down = True

            self.key_map[key].down = is_key_down
            self.key_map[key].log.append(
                KeyPressLogRecord(dt=ticks, down=is_key_down, processed=False))

        self.flush()

    def read(self, start: int, end: int) -> dict[int, KeyPressLog]:
        sliced = {}

        for key, value in self.key_map.items():
            before: list[KeyPressLogRecord] = []
            for log in value.log:
                if start <= log.dt < end and not log.processed:
                    log.processed = True
                    before.append(log)

            if len(before) > 0:
                sliced[key] = KeyPressLog(
                    down=before[-1].down,
                    interval=value.interval,
                    log=before,
                    subscriber=value.subscriber,
                    updated=before[-1].dt,
                )

        return sliced





