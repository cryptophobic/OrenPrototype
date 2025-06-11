from app.journal.journal import Logging


class Actor(Logging):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.active = True
        self.dirty = False
        self.behaviors = {}
