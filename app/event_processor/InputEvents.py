from collections import namedtuple, deque

import pygame
from app.event_processor.Timer import Timer
from typing import Dict, Tuple, List
from dataclasses import dataclass
from app.event_processor.Gamepads import Gamepads
from app.event_processor.Scheduler import Scheduler
# Removed ui dependencies for generic event processing


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

KeyPressDetails = namedtuple("KeyPressDetails", ["key", "repeat_delta"])
EventLogRecord = namedtuple("EventLogRecord", ["dt", "key", "down"])

# This function will be replaced by behavior-based key extraction


class InputEvents:

    flushing_interval = 10000

    def __init__(self):
        self.scheduler = Scheduler()
        self.gamepads = Gamepads()
        self.subscribers: Dict[str, Tuple] = {}
        self.key_map: Dict[int, KeyPressLog] = {}
        self.keys_down: List[int] = []
        self.next_flush = Timer.current_timestamp() + InputEvents.flushing_interval

    def subscribe(self, subscriber_name: str, keys: List[Tuple[int, int]]):
        """Subscribe to keys with (key_code, repeat_delta) tuples"""
        if subscriber_name in self.subscribers:
            return False

        for key, repeat_delta in keys:
            if self.key_map.get(key) is None:
                self.key_map[key] = KeyPressLog(down=False, subscribers=0, log=[], interval=repeat_delta)
            self.key_map[key].subscribers += 1

        self.subscribers[subscriber_name] = tuple(k[0] for k in keys)
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
        pressed = pygame.key.get_pressed()
        for idx, key in enumerate(self.keys_down):

            if key not in self.key_map:
                self.keys_down.pop(idx)
                continue

            if (self.is_down_event_expired(key)
                    or (not pressed[key] and not self.scheduler.is_pressed(key) and not self.gamepads.pressed(key))):
                self.key_map[key].down = False
                self.key_map[key].log.append(KeyPressLogRecord(dt=ticks, down=False, processed=False))
                self.keys_down.pop(idx)

        for key, events_log in self.key_map.items():
            if (events_log.down is not True
                    and (pressed[key] or self.scheduler.is_pressed(key) or self.gamepads.pressed(key))):

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
            )

        return sliced

    def slice_flat(self, start: int, end: int) -> deque[EventLogRecord]:
        flushed = self.slice(start, end)

        return deque(sorted(
            (log_entry.dt, key, log_entry.down)
            for key, value in flushed.items()
            for log_entry in value.log
            if start <= log_entry.dt
        ))

    def slice_grouped(self, start: int, end: int) -> Dict[int, List[KeyPressLogRecord]]:
        flushed = self.slice(start, end)

        return {
            key:
                list(filter(lambda log_entry: (start <= log_entry.dt), value.log))
            for key, value in flushed.items()
        }
