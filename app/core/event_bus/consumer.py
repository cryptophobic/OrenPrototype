from typing import Optional, Dict, Callable, Any

from app.core.event_bus.bus import EventBus
from app.core.event_bus.events import Events


class Consumer:

    def __init__(self):
        self._event_bus: Optional[EventBus] = None
        self._handlers: Dict[Events, Callable[[Any], None]] = {}

    def register_event_bus(self, event_bus: EventBus):
        self._event_bus = event_bus
        for event_type, handler in self._handlers.items():
            self._event_bus.subscribe(event_type, handler)

    def register_handler(self, event_type: Events, handler: Callable[[Any], None]):
        self._handlers[event_type] = handler
        if self._event_bus:
            self._event_bus.subscribe(event_type, handler)

    def unregister_handler(self, event_type: Events, handler: Callable[[Any], None]):
        self._handlers.pop(event_type, None)
        if self._event_bus:
            self._event_bus.unsubscribe(event_type, handler)
