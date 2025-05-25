from ui.actors.actions import Actions
from ui.actors.body import Body
from ui.actors.controls import Controls


class Actor:
    def __init__(self):
        self.prio: int = 0
        self.active: bool = False
        self.name: str | None = None
        self.actions: Actions | None = None
        self.controls: Controls | None = None
        self.body: Body | None = None
        pass

    def get_action(self, key: int):
        return self.controls.get(key)

    def is_conflicting(self, actor: 'Actor') -> bool:
        return actor.active and self.active and self.body.collision_matrix.blocks(actor.body.collision_matrix)

    def is_overlapping(self, actor: 'Actor') -> bool:
        return actor.active and self.active and self.body.collision_matrix.overlaps(actor.body.collision_matrix)
