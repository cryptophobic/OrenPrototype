from dataclasses import dataclass
from enum import Enum, auto
from collections import deque
from typing import Dict


class ObjectTypes(Enum):
    PROPERTY = auto()
    METHOD = auto()

class ObjectActions(Enum):
    READ = auto()
    WRITE = auto()
    CALL = auto()

@dataclass
class EventLogRecord:
    dt: int
    object_id: str
    object_type: ObjectTypes
    action: ObjectActions
    extra: dict | None = None

class EventLog(deque[EventLogRecord]):
    pass

class Journal(Dict[str, EventLog]):
    def log_append(self, name: str, event_log_record: EventLogRecord):
        if name not in self:
            self[name] = EventLog()
        self[name].append(event_log_record)
    pass

journal = Journal()


def is_internal(name: str) -> bool:
    return name.startswith("_")


class Logging:
    def __init__(self, name: str = "global"):
        self._journal = journal
        self.__name: str = name
        self.__disable_read_events: bool = True

    @property
    def _context(self):
        from app.context.frame_context import FrameContext
        return FrameContext.instance()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __getattribute__(self, name):
        if is_internal(name):
            return super().__getattribute__(name)

        attr = super().__getattribute__(name)
        if callable(attr):
            def wrapped(*args, **kwargs):
                event_log = EventLogRecord(
                    dt=self._context.timestamp,
                    object_id=name,
                    object_type=ObjectTypes.METHOD,
                    action=ObjectActions.CALL,
                    extra={"args": args, "kwargs": kwargs}
                )
                self._journal.log_append(self.__name, event_log)
                return attr(*args, **kwargs)
            return wrapped
        elif not self.__disable_read_events:
            event_log = EventLogRecord(
                dt=self._context.timestamp,
                object_id=name,
                object_type=ObjectTypes.PROPERTY,
                action=ObjectActions.READ
            )
            self._journal.log_append(self.__name, event_log)

        return attr

    def __setattr__(self, name, value):
        if not is_internal(name):
            old_value = getattr(self, name, None)
            event_log = EventLogRecord(
                dt=self._context.timestamp,
                object_id=name,
                object_type=ObjectTypes.PROPERTY,
                action=ObjectActions.WRITE,
                extra={"old": old_value, "new": value}
            )
            self._journal.log_append(self.__name, event_log)

        super().__setattr__(name, value)
