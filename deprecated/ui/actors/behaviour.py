from deprecated.ui.actors.actor import Actor

class Behaviour:
    def __init__(self, actor: Actor):
        self.actor = actor

    def update(self):
        pass
