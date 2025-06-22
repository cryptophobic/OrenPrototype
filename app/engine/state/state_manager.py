from collections import deque
from .events_handler import EventsHandler
from .event_bus import EventBus
from .grid import Grid
from ...objects.actor import Actor


class StateManager:
    def __init__(self):
        pass

    def update_state(self, events: deque):
        """Process dirty actors and dispatch events"""
        # Process dirty actors first
        for actor in self.actors.get_dirty_actors():
            self.events_handler.unload_keys_from_actor(actor)
            self.events_handler.load_keys_from_actor(actor)
            if hasattr(actor, 'dirty'):
                actor.dirty = False

        # Dispatch input events
        self.events_handler.dispatch_events(events)

    def commit(self) -> bool:
        """Process all actions and return True if state changed"""
        return self.event_bus.process_actions()

    def get_actor(self, name: str):
        """Get actor by name"""
        return self.actors.get(name)

    def get_all_actors(self):
        """Get all registered actors"""
        return list(self.actors.values())

    def get_active_actors(self):
        """Get all active actors"""
        return self.actors.get_active_actors()