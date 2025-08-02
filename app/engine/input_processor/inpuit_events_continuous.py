from dataclasses import dataclass

from app.core.types import ContinuousKeyPressEventLogRecords, ContinuousKeyPressEventLogRecord
from app.engine.message_broker.types import Controls


@dataclass(order=True)
class KeyPressLogRecord:
    dt: int
    micro_tick: int
    down: bool
    processed: bool = False


@dataclass
class KeyPressLog:
    interval: int
    subscriber: str
    log: list[KeyPressLogRecord]

@dataclass
class KeysUpDownState:
    down: dict[int, int]
    up: dict[int, int]

class InputEventsContinuous:
    flushing_interval = 10000

    def __init__(self, timestamp: int = 0):
        self.subscribers: dict[str, tuple[int, ...]] = {}
        self.key_map: dict[int, KeyPressLog] = {}
        self.next_flush = timestamp + self.flushing_interval
        self.last_timestamp: int = -1
        self.micro_tick: int = 0

        self.key_pressed: set[int] = set()

    def subscribe(self, subscriber_name: str, keys: Controls):
        for key, binding in keys.items():
            if self.key_map.get(key) is None:
                self.key_map[key] = KeyPressLog(
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

    def flush(self, timestamp: int):
        if timestamp > self.next_flush:
            frame = max(0, self.next_flush - self.flushing_interval)
            for value in self.key_map.values():
                value.log = [log for log in value.log if log.dt >= frame]

            self.next_flush = timestamp + self.flushing_interval

    def _put_new_record_to_log(self, key: int, timestamp: int, down: bool):
        if timestamp != self.last_timestamp:
            self.last_timestamp = timestamp
            self.micro_tick = 0
        else:
            self.micro_tick += 1

        self.key_map[key].log.append(
            KeyPressLogRecord(dt=timestamp, micro_tick=self.micro_tick, down=down))


    '''
    is called from GameView.on_key_press, GameView.on_key_release
    '''
    def register_key_pressed(self, key: int, down: bool, timestamp: int):
        if not key in self.key_map:
            return

        if not down:
            self.key_pressed.discard(key)
        else:
            self.key_pressed.add(key)

        self._put_new_record_to_log(key, timestamp, down)

    def listen(self, timestamp: int):
        pressed = self.key_pressed

        for key in pressed:
            key_map = self.key_map.get(key)

            if key_map is None:
                continue

            last_log = key_map.log[-1] if key_map.log else None

            if key_map.interval < 0 and last_log and last_log.down:
                continue

            if last_log and last_log.dt > timestamp - key_map.interval:
                continue

            self._put_new_record_to_log(key, timestamp, True)

        self.flush(timestamp)

    def read(self, start: int, end: int) -> dict[str, ContinuousKeyPressEventLogRecords]:
        sliced = {}

        for key, value in self.key_map.items():
            for log in value.log:
                if start <= log.dt < end and not log.processed:
                    log.processed = True
                    sliced.setdefault(value.subscriber, ContinuousKeyPressEventLogRecords()).append(
                        ContinuousKeyPressEventLogRecord(
                            dt=(log.dt, log.micro_tick), key=key, down=log.down
                        )
                    )

        return sliced
