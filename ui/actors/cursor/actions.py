from ui.actors.actions import Actions as BaseActions

class Actions(BaseActions):

    def move_left(self):
        self.actor.body.velocity.x -= 1
        pass

    def move_right(self):
        self.actor.body.velocity.x += 1
        pass

    def move_up(self):
        self.actor.body.velocity.y -= 1
        pass

    def move_down(self):
        self.actor.body.velocity.y += 1
        pass

    def commit(self):
        #
        self.actor.body.coordinates += self.actor.body.velocity
        pass
