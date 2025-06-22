from collections import deque
from typing import Dict, Set


class EventsHandler:
    def __init__(self, actors_collection):
        self.actors = actors_collection
        self.__keys: Dict[int, Set[str]] = {}  # pygame key -> actor names

    def load_keys_from_actor(self, actor):
        """Load key mappings from Player behavior of actor"""
        if hasattr(actor, 'behaviors') and "player" in actor.behaviors:
            player_behavior = actor.behaviors["player"]
            if hasattr(player_behavior, 'get_actions'):
                for key, action in player_behavior.get_actions().items():
                    if key not in self.__keys:
                        self.__keys[key] = set()
                    self.__keys[key].add(actor.name)

    def unload_keys_from_actor(self, actor):
        """Remove all key mappings for this actor"""
        for key_set in self.__keys.values():
            key_set.discard(actor.name)

    def dispatch_events(self, events: deque):
        """Process events for Player-controlled actors only"""
        # This will be implemented when we have the event structure
        # For now, just a placeholder
        for event in events:
            if hasattr(event, 'key') and event.key in self.__keys:
                for actor_name in self.__keys[event.key]:
                    if actor_name in self.actors:
                        actor = self.actors[actor_name]
                        if hasattr(actor, 'get_action'):
                            action = actor.get_action(event.key)
                            if action:
                                # Queue action to event bus
                                pass