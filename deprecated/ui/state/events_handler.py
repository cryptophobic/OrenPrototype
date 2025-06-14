from collections import deque
from typing import Dict, Callable

from deprecated.event_processor.InputEvents import EventLogRecord
from deprecated.ui.actors.actor import Actor
from deprecated.ui.state.actors_collection import ActorsCollection
from deprecated.ui.state.event_bus import EventBus



class EventsHandler:
    def __init__(self, actors: ActorsCollection, conflict_resolver: Callable):
        self.actors: ActorsCollection = actors
        self.event_bus: EventBus = EventBus(conflict_resolver)
        self.__keys: Dict[int: set[str]] = {}

    def dispatch_events(self, events: deque[EventLogRecord]) -> None:
        while events:
            print(events)

            _, key, down = events.popleft()
            if not down:
                continue
            actor_names = self.__keys.get(key)
            if actor_names is None:
                continue

            for actor_name in actor_names:
                actor = self.actors.get(actor_name)
                if actor is None or actor.active is False:
                    continue

                self.event_bus.post(actor, actor.get_action(key))

    def process_events(self) -> bool:
        return self.event_bus.flush() > 0

    def load_keys_from_actor(self, actor: Actor):
        for key in actor.controls.keys():
            self.add_key(key, actor.name)

    def unload_keys_from_actor(self, actor: Actor):
        for key in actor.controls.keys():
            self.remove_key(key, actor.name)

    def add_key(self, key: int, actor_name: str):
        if self.__keys.get(key) is None:
            self.__keys[key] = set()
        self.__keys[key].update({actor_name})

    def remove_key(self, key: int, actor_name: str = ""):
        if actor_name == "":
            self.__keys.pop(key, None)
            return

        set_of_actors = self.__keys.get(key)
        if set_of_actors is not None and actor_name in set_of_actors:
            set_of_actors.remove(actor_name)

        if len(set_of_actors) == 0:
            self.__keys.pop(key, None)
