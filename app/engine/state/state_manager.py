from collections import deque
from .actors_collection import ActorsCollection
from .events_handler import EventsHandler
from .event_bus import EventBus


class StateManager:
    def __init__(self, grid=None):
        self.grid = grid
        self.actors = ActorsCollection()
        self.events_handler = EventsHandler(self.actors)
        self.event_bus = EventBus(self.grid)

    def register_actor(self, actor):
        """Register an actor in the system"""
        name = self.actors.add_actor(actor)
        self.events_handler.load_keys_from_actor(actor)
        return name

    def remove_actor(self, actor):
        """Remove an actor from the system"""
        if hasattr(actor, 'name') and actor.name:
            self.events_handler.unload_keys_from_actor(actor)
            self.actors.remove_actor(actor.name)

    def queue_action(self, actor, action):
        """Safe API for AI action injection"""
        self.event_bus.post(actor, action)

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