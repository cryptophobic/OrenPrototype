from collections import deque
from typing import Dict

from deprecated.ui.actors.actions import Actions
from deprecated.ui.actors.behaviour import Behaviour
from deprecated.ui.actors.body import Body
from deprecated.ui.actors.controls import Controls
from deprecated.ui.actors.vectors import Vec2
from deprecated.ui.config import Behaviours


class Actor:
    def __init__(self, coordinates: Vec2):
        self.prio: int = 0
        self.active: bool = True
        self.name: str | None = None
        self.actions: Actions | None = None
        self.controls: Controls | None = None
        self.body: Body | None = None
        self.coordinates: Vec2 = coordinates
        self.track: deque[Vec2] = deque()
        self.__behaviours: Dict[Behaviours, Behaviour] = {}

    def is_behaves(self, behaviour: Behaviours) -> bool:
        return behaviour in self.__behaviours

    

    def clear_velocity(self):
        self.actions.clear_velocity()

    def current_velocity(self) -> Vec2:
        return self.actions.current_velocity()

    def get_action(self, key: int):
        return self.controls.get(key)

    def is_conflicting(self, actor: 'Actor') -> bool:
        return actor.active and self.active and self.body.collision_matrix.blocks(actor.body.collision_matrix)

    def is_overlapping(self, actor: 'Actor') -> bool:
        return actor.active and self.active and self.body.collision_matrix.overlaps(actor.body.collision_matrix)
