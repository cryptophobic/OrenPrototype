from ui.actors.vectors import Vec2


class Body:
    def __init__(self):
        self.shape = None
        self.velocity: Vec2 = Vec2(x=0, y=0)
        pass

    def is_dirty(self):
        return self.velocity.is_dirty()