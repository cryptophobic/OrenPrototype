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

class EventLog(deque):
    pass

class Journal(Dict[str, EventLog]):
    pass

class GlobalJournal(Journal):
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
