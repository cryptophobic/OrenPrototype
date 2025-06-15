from collections import deque
from typing import Deque, Optional, List

from ...bus.command_pipeline import ActorAction
from ...config import Behaviours
from ...engine.state.event_bus import ActionFn, Message
from ...journal.journal import Logging
from ...objects.behaviors.behaviour import Behaviour


class Actor(Logging):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.active = True
        self.blocking_actions: deque[ActorAction] = deque()
        self.pending_actions: Deque[ActionFn]
        self.__behaviours: dict[Behaviours, Behaviour] = {}

    def is_behave_as_this(self, behaviour: Behaviours) -> bool:
        return self.is_behave_as_them([behaviour])

    def get_behaviour(self, behaviour: Behaviours) -> Optional[Behaviour]:
        return self.__behaviours[behaviour]

    def is_behave_as_them(self, behaviours: List[Behaviours]) -> bool:
        return all(behaviour in self.__behaviours for behaviour in behaviours)

    def add_behaviour(self, behaviour: Behaviour):
        self.__behaviours[behaviour.name] = behaviour
        return self

    def remove_behaviour(self, behaviour: Behaviour):
        self.__behaviours.pop(behaviour.name, None)
        return self

    def add_pending_action(self, action: ActionFn):
        self.pending_actions.append(action)

    def commit_actions(self) -> Optional[Message]:
        while len(self.pending_actions) > 0:
            # This is very unobvious, action must be a method from one of behaviours
            # It came from EventBus
            # And the thing is that I don't know how to control it.
            # How to make sure this action is an action of connected behaviour.
            # One of possible solutions I consider introducing
            # Action class with behaviour name, method name and arguments
            action = self.pending_actions.popleft()
            conflict_resolver = action()
            if conflict_resolver is not None:
                self.pending_actions.clear()
                return conflict_resolver

        return None
