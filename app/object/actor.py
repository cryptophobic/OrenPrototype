class Actor:
    def __init__(self, name: str = None):
        self.name = name
        self.active = True
        self.dirty = False
        self.behaviors = {}
