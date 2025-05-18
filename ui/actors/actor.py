from ui.actors.body import Body
from ui.actors.controls import Controls


class Actor:
    def __init__(self, name: str = None):
        self.prio: int = 0
        self.active: bool = True
        self.name: str = name
        self.controls: Controls = Controls()
        self.body: Body = Body()
        pass