from app.helpers.collection_base import CollectionBase
from app.helpers.unique_name import generate_unique_name
from app.objects.actor.actor import Actor
from typing import TypeVar, Generic

T = TypeVar("T", bound=Actor)

class ActorsCollection(CollectionBase[T], Generic[T]):
    def __init__(self, items: dict[str, Actor] | None = None):
        super().__init__(items or {})

    def get_active_actors(self) -> "ActorsCollection":
        return ActorsCollection(self.filter(lambda a: a.active))

    def add(self, actor: T):
        if actor.name and actor.name not in self.data:
            name = actor.name
        else:
            name = generate_unique_name(set(self.data.keys()))
            actor.name = name

        self.data[name] = actor

