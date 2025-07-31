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
    log: list[KeyPressLogRecord]
    subscriber: str

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

        self.keys_down: dict[int, int] = {}
        self.keys_up: dict[int, int] = {}

        self.key_pressed: set[int] = set()


    def subscribe(self, subscriber_name: str, keys: Controls):
        for key, binding in keys.items():
            if self.key_map.get(key) is None:
                self.key_map[key] = KeyPressLog(
                    subscriber=subscriber_name,
                    log=[],
                    interval=binding.repeat_delta
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

    def is_key_down(self, key: int) -> bool:
        down = self.keys_down.get(key, 0)
        up = self.keys_up.get(key, 0)
        return down > up

    def is_down_event_expired(self, key: int) -> bool:
        if not self.is_key_down(key):
            return False

        key_map = self.key_map.get(key)
        if key_map is None or key_map.interval < 0:
            return False

        if self.keys_down[key] <= self.ticks - key_map.interval:
            return True

        return False

    def listen(self, ticks: int):
        self.ticks = ticks
        pressed = self.key_pressed

        for key in pressed:
            is_key_down = self.is_key_down(key)

            if is_key_down:
                is_key_down = not self.is_down_event_expired(key)

            if is_key_down:
                self.keys_down[key] = ticks
            else:
                self.keys_up[key] = ticks

            '''
            Not sure if I would need this.
            What could I achieve with the information 
            about the key repeatedly pressed during the ONE frame.
            '''
            self.key_map[key].down = is_key_down
            self.key_map[key].log.append(
                KeyPressLogRecord(dt=ticks, down=is_key_down, processed=False))

        self.flush()

    def read(self, start: int, end: int) -> KeysUpDownState:
        sliced = {}

        for key, value in self.key_map.items():
            before = []
            for log in value.log:
                if start <= log.dt < end and not log.processed:
                    log.processed = True
                    before.append(log)

            sliced[key] = KeyPressLog(
                down=before[-1].down if len(before) > 0 else False,
                interval=value.interval,
                log=before,
                subscriber=value.subscribers,

            )

        return KeysUpDownState(
            down=self.keys_down,
            up=self.keys_up,
        )





