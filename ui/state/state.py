from collections import deque

from event_processor.InputEvents import EventLogRecord
from ui.actors.actor import Actor
from ui.state.actors_collection import ActorsCollection
from ui.state.events_handler import EventsHandler


def conflict_resolver(actor1: Actor, actor2: Actor):
    if actor1.is_conflicting(actor2):
        actor1.clear_velocity()
        actor2.clear_velocity()


class State:
    def __init__(self):
        self.actors: ActorsCollection = ActorsCollection()
        self.__events_handler = EventsHandler(self.actors, conflict_resolver)

    def register_actor(self, actor: Actor):
        self.actors.add(actor)
        self.__events_handler.load_keys_from_actor(actor)

    def remove_actor(self, actor: Actor):
        self.actors.remove(actor)
        self.__events_handler.unload_keys_from_actor(actor)

    def update_state(self, events: deque[EventLogRecord]):
        self.__events_handler.dispatch_events(events)

    def commit(self) -> bool:
        return self.__events_handler.process_events()
