import random
from collections import UserDict
from ui.actors.actor import Actor
import petname


class ActorsCollection(UserDict):
    def __init__(self):
        super().__init__()

    def idle_actors(self):
        return filter(lambda x: x.idle, self.data.values())

    def to_render_actors(self):
        return list(filter(lambda x: x.idle is False, self.data.values()))

    def sorted_dirty_actors(self):
        def is_dirty(actor: Actor) -> bool:
            return actor.active is True and (actor.body.is_dirty())

        return sorted(filter(is_dirty, self.data.values()), key=lambda x: x.prio, reverse=True)

    def add(self, actor: Actor):
        while not actor.name or actor.name in self.data:
            name = petname.Generate(2, separator="-")
            name = f"{name}-{random.randint(100, 999)}"
            actor.name = name

        self.data[actor.name] = actor

    def remove(self, actor: Actor):
        self.data.pop(actor.name, None)
