from collections import defaultdict
from typing import Callable, Dict, List, Any

from app.core.event_bus.events import Events


class EventBus:
    def __init__(self):
        self.subscribers: Dict[Events, List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event_type: Events, callback: Callable[[Any], None]):
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: Events, callback: Callable[[Any], None]):
        if callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)

    def publish(self, event_type: Events, payload: Any):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(payload)
