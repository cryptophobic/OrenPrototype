from typing import Dict, List

from event_processor.InputEvents import KeyPressLog
from ui.actors.actor import Actor
from ui.state.actors_collection import ActorsCollection


class EventsHandler:
    def __init__(self, actors: ActorsCollection):
        self.actors: ActorsCollection = actors
        self.__keys: Dict[int: set[str]] = {}

    def dispatch_events(self, events: Dict[int, List[KeyPressLog]]) -> None:
        for key, events_log in events.items():
            if len(events_log) == 0:
                continue
            actor_names = self.__keys.get(key)
            if actor_names is None:
                continue

            for actor_name in actor_names:
                self.update_actor(actor_name, key, events_log)

    def update_actor(self, actor_name: str, key: int, events_log: List[KeyPressLog]) -> None:
        for event in events_log:
            if event.down is not True:
                continue

            actor = self.actors.get(actor_name)
            if actor is None or actor.idle:
                continue

            actor.dispatch(key)

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
