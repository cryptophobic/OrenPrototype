from collections import deque, UserDict
from dataclasses import dataclass, field
from typing import Callable, Deque, TypeVar, Optional, Dict

from ...objects.actor.actor import Actor
from ...objects.actors_collection import ActorsCollection
from ...context.frame_context import FrameContext

class Diff(UserDict[str, str]):
    pass

T = TypeVar("T", bound=ActorsCollection)
ActionFn = Callable[[T], Optional["Message"]]

@dataclass
class Message:
    sender: Actor
    action: ActionFn
    receivers: ActorsCollection = field(default_factory=ActorsCollection)
    attempts_to_process: int = 2


@dataclass
class Banned:
    sender: Actor
    receivers: ActorsCollection
    till: int = 0


class EventBus:
    def __init__(self):
        self._queue: Deque[Message] = deque()
        self.__banned: Dict[str, Banned] = {}

    def post(self, message: Message):
        """Add action to the queue"""
        self._queue.append(message)

    def put_to_ban(self, sender: Actor, receivers: ActorsCollection, till: int = 0):
        self.__banned[sender.name] = Banned(sender, receivers, till)

    def clean_bans(self):
        now = FrameContext.instance().timestamp
        self.__banned = {k: v for k, v in self.__banned.items() if v.till > now}

    def filter_banned_receivers(self, actor: Actor, actors_collection: ActorsCollection) -> ActorsCollection:
        banned = actor.name in self.__banned and self.__banned[actor.name].till <= FrameContext.instance().timestamp
        return actors_collection if not banned else actors_collection.subtract_actors(self.__banned[actor.name].receivers)

    def process_actions(self) -> bool:
        state_changed = False

        while self._queue:
            message = self._queue.popleft()
            if message.attempts_to_process <= 0:
                continue

            actor = message.sender
            action = message.action

            actor.add_pending_action(message)

            action(message.receivers)
            conflict_resolver = actor.commit_actions()
            message.attempts_to_process -= 1
            if conflict_resolver:
                receivers = self.filter_banned_receivers(actor, conflict_resolver.receivers)
                if receivers:
                    conflict_resolver.receivers = receivers
                    self.put_to_ban(sender=actor, receivers=conflict_resolver.receivers, till=FrameContext.instance().timestamp)
                    self._queue.appendleft(message)
                    self._queue.appendleft(conflict_resolver)

                continue

            # Maybe later access the Journal to track the changing state
            state_changed = True

        return state_changed

    def clear_queue(self):
        """Clear all pending actions"""
        self._queue.clear()
