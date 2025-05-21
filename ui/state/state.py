from typing import List, Dict
from collections import deque


from event_processor.InputEvents import KeyPressLog
from ui.actors.actor import Actor
from ui.state.actors_collection import ActorsCollection
from ui.state.events_handler import EventsHandler


class State:
    def __init__(self):
        self.actors: ActorsCollection = ActorsCollection()
        self.__events_handler = EventsHandler(self.actors)

    def register_actor(self, actor: Actor):
        self.actors.add(actor)
        self.__events_handler.load_keys_from_actor(actor)

    def remove_actor(self, actor: Actor):
        self.actors.remove(actor)
        self.__events_handler.unload_keys_from_actor(actor)

    def update_state(self, events: Dict[int, List[KeyPressLog]]):
        self.__events_handler.dispatch_events(events)

    def commit(self) -> bool:
        committed = False

        for actor in self.actors.sorted_dirty_actors():
            actor.
            actor.active = False
            pass

        while self.__events_array:
            events = self.__events_array.popleft()
            committed = committed or self.__events_handler.dispatch_events(events)

        return committed
