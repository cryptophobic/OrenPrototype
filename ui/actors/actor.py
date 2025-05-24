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

    def dispatch(self, key: int):
        self.controls.action(key)