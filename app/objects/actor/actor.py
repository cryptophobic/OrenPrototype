from collections import deque
from typing import List

from ...behaviors.behaviours_collection import BehavioursCollection
from ...bus.message_broker.types import Message, Promise
from ...config import Behaviours
from ...journal.journal import Logging
from ...behaviors.behaviour import Behaviour, BehaviourAction


class Actor(Logging):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.active = True
        self.blocking_actions: deque[BehaviourAction] = deque()
        self.__behaviours: BehavioursCollection = BehavioursCollection()

    def on_message(self, message: Message) -> Promise:
        filtered_behaviours = self.__behaviours.can_response_to(message.message_type)
        response_actions: deque[BehaviourAction] = deque()
        for behaviour in filtered_behaviours.values():
            response_actions.extend(behaviour.on_message(self, message))

        return Promise(
            responder=self,
            response_actions=response_actions,
            reason=f"{self.name} received {message.message_type}")

    def is_behave_as_this(self, behaviour: Behaviours) -> bool:
        return self.is_behave_as_them([behaviour])

    def is_behave_as_them(self, behaviours: List[Behaviours]) -> bool:
        return all(behaviour in self.__behaviours for behaviour in behaviours)

    def add_behaviour(self, behaviour: type[Behaviour]):
        self.__behaviours[behaviour.name] = behaviour
        return self

    def remove_behaviour(self, behaviour: type[Behaviour]):
        self.__behaviours.pop(behaviour.name, None)
        return self
