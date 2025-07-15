from collections import deque

from typing import Dict, Tuple, List
from dataclasses import dataclass

from app.core.types import KeyPressEventLogRecords, KeyPressEventLogRecord
from app.engine.input_processor.Gamepads import Gamepads
from app.engine.input_processor.Scheduler import Scheduler
from app.engine.input_processor.Timer import Timer
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
    log: List[KeyPressLogRecord]
    subscribers: int
    subscribers_set: set[str]

class InputEvents:

    flushing_interval = 10000

    def __init__(self):
        self.scheduler = Scheduler()
        self.gamepads = Gamepads()
        self.subscribers: Dict[str, Tuple] = {}
        self.key_map: Dict[int, KeyPressLog] = {}
        self.keys_down: List[int] = []
        self.next_flush = Timer.current_timestamp() + InputEvents.flushing_interval
        self.key_pressed: dict[int, bool] = {}

    def subscribe(self, subscriber_name: str, keys: Controls):
        if subscriber_name in self.subscribers:
            return False

        for key, binding in keys.items():
            if self.key_map.get(key) is None:
                self.key_map[key] = KeyPressLog(
                    down=False,
                    subscribers=0,
                    subscribers_set={subscriber_name},
                    log=[],
                    interval=binding.repeat_delta
                )
            self.key_map[key].subscribers += 1

        self.subscribers[subscriber_name] = tuple(k for k in keys.keys())
        return True

    def unsubscribe(self, subscriber: str):
        if subscriber not in self.subscribers:
            return False

        for key in self.subscribers[subscriber]:
            if key not in self.key_map:
                continue

            if self.key_map[key].subscribers == 1:
                del self.key_map[key]
                continue

            self.key_map[key].subscribers -= 1
            self.key_map[key].subscribers_set.remove(subscriber)

        return True

    def is_down_event_expired(self, key: int) -> bool:
        key_map = self.key_map.get(key)
        if key_map is None or key_map.interval < 0 or key_map.down is False or len(key_map.log) == 0:
            return False

        last_event = key_map.log[-1]

        if last_event.dt <= Timer.current_timestamp() - key_map.interval:
            return True

        return False

    def flush(self):
        if Timer.current_timestamp() > self.next_flush:
            frame = max(0, self.next_flush - InputEvents.flushing_interval)
            for value in self.key_map.values():
                value.log = [log for log in value.log if log.dt >= frame]

            self.next_flush = Timer.current_timestamp() + InputEvents.flushing_interval

    def listen(self, ticks: int):
        pressed = self.key_pressed
        for idx, key in enumerate(self.keys_down):

            if key not in self.key_map:
                self.keys_down.pop(idx)
                continue

            key_pressed = pressed.get(key, False)

            if (self.is_down_event_expired(key)
                    or (not key_pressed and not self.scheduler.is_pressed(key) and not self.gamepads.pressed(key))):
                self.key_map[key].down = False
                self.key_map[key].log.append(KeyPressLogRecord(dt=ticks, down=False, processed=False))
                self.keys_down.pop(idx)

        for key, events_log in self.key_map.items():
            key_pressed = pressed.get(key, False)

            if (events_log.down is not True
                    and (key_pressed or self.scheduler.is_pressed(key) or self.gamepads.pressed(key))):

                self.key_map[key].down = True
                self.key_map[key].log.append(KeyPressLogRecord(dt=ticks, down=True, processed=False))
                self.keys_down.append(key)

        self.flush()

    def slice(self, start: int, end: int) -> Dict[int, KeyPressLog]:
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
                subscribers=value.subscribers,
                subscribers_set=value.subscribers_set,
            )

        return sliced

    def slice_flat(self, start: int, end: int) -> KeyPressEventLogRecords:
        flushed = self.slice(start, end)

        return deque(sorted(
            (
                KeyPressEventLogRecord(log_entry.dt, key, log_entry.down, value.subscribers_set)
                for key, value in flushed.items()
                for log_entry in value.log
                if start <= log_entry.dt
            ),
            key=lambda r: r.dt
        ))

    def slice_grouped(self, start: int, end: int) -> Dict[int, List[KeyPressLogRecord]]:
        flushed = self.slice(start, end)

        return {
            key:
                list(filter(lambda log_entry: (start <= log_entry.dt), value.log))
            for key, value in flushed.items()
        }
