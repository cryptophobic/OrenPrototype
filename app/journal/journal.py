from dataclasses import dataclass
from enum import Enum, auto
from collections import deque
from typing import Dict

from app.context.context import Context


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

class Logging:
    def __init__(self, name: str = "global"):
        self._journal = journal
        self.__context = Context.instance()
        self.name: str = name

    def __is_internal(self, name: str) -> bool:
        return name.startswith("_") and name not in {"name"}

    def __getattribute__(self, name):
        if self.__is_internal(name):
            return super().__getattribute__(name)

        attr = super().__getattribute__(name)
        if callable(attr) and not name.startswith("__"):
            def wrapped(*args, **kwargs):
                event_log = EventLogRecord(
                    dt=self.__context.frame_context.timestamp,
                    object_id=name,
                    object_type=ObjectTypes.METHOD,
                    action=ObjectActions.CALL,
                    extra={"args": args, "kwargs": kwargs}
                )
                self._journal.log_append(self.name, event_log)
                return attr(*args, **kwargs)
            return wrapped
        else:
            event_log = EventLogRecord(
                dt=self.__context.frame_context.timestamp,
                object_id=name,
                object_type=ObjectTypes.PROPERTY,
                action=ObjectActions.READ
            )
            self._journal.log_append(self.name, event_log)

        return attr

    def __setattr__(self, name, value):
        if not self._is_internal(name):
            old_value = getattr(self, name, None)
            event_log = EventLogRecord(
                dt=self.__context.frame_context.timestamp,
                object_id=name,
                object_type=ObjectTypes.PROPERTY,
                action=ObjectActions.WRITE,
                extra={"old": old_value, "new": value}
            )
            self._journal.log_append(self.name, event_log)

        super().__setattr__(name, value)
