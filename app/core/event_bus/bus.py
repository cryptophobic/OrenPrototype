from collections import defaultdict
from enum import Enum, auto
from typing import Callable, Dict, List, Any

from app.core.event_bus.events import Events

class Strategies(Enum):
    AtMostOnce = auto()
    AtLeastOnce = auto()
    ExactlyOnce = auto()

class EventBus:
    def __init__(self):
        self.subscribers: Dict[Events, List[Callable[[Any], None]]] = defaultdict(list)
        self._pending_events: Dict[Events, List[Any]] = defaultdict(list)

    def subscribe(self, event_type: Events, callback: Callable[[Any], None]):
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: Events, callback: Callable[[Any], None]):
        if callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)

    def emit(self, event_type: Events, payload: Any, strategy: Strategies = Strategies.AtMostOnce) -> None:
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(payload)
        else:
            match strategy:
                case Strategies.AtMostOnce:
                    return
                case Strategies.ExactlyOnce:
                    return


# SINGLE shared bus
bus = EventBus()
