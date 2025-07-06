from collections import deque
from typing import List

from ...behaviors.behaviours_collection import BehavioursCollection
from ...bus.message_broker.types import MessageBody
from ...config import Behaviours
from ...context.behaviour_registry import get_registry
from ...journal.journal import Logging
from ...behaviors.behaviour import Behaviour, BehaviourAction

class Actor(Logging):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.active = True
        self.pending_actions: deque[BehaviourAction] = deque()
        self.__behaviours: BehavioursCollection = BehavioursCollection()

    def on_message(self, message_body: MessageBody) -> deque[BehaviourAction]:
        filtered_behaviours = self.__behaviours.can_response_to(message_body.message_type)
        response_actions: deque[BehaviourAction] = deque()
        for behaviour in filtered_behaviours.values():
            response_actions.extend(behaviour.on_message(self, message_body))

        return response_actions

    def is_behave_as_this(self, behaviour: Behaviours) -> bool:
        return self.is_behave_as_them([behaviour])

    def is_behave_as_them(self, behaviours: List[Behaviours]) -> bool:
        return all(behaviour in self.__behaviours for behaviour in behaviours)

    def add_behaviour_from_enum(self, behaviour: Behaviours):
        behaviour_class = get_registry().get(behaviour)
        return self.add_behaviour(behaviour_class)

    def add_behaviour(self, behaviour: type[Behaviour]):
        self.__behaviours[behaviour.name] = behaviour
        return self

    def remove_behaviour(self, behaviour: type[Behaviour]):
        self.__behaviours.pop(behaviour.name, None)
        return self
