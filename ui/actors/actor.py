from ui.actors.actions import Actions
from ui.actors.body import Body
from ui.actors.controls import Controls
from ui.actors.vectors import Vec2


class Actor:
    def __init__(self, coordinates: Vec2):
        self.prio: int = 0
        self.active: bool = True
        self.name: str | None = None
        self.actions: Actions | None = None
        self.controls: Controls | None = None
        self.body: Body | None = None
        self.coordinates: Vec2 = coordinates

        pass

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
