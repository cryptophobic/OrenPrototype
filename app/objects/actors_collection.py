from typing import TypeVar, Generic, Self
from app.helpers.collection_base import CollectionBase
from app.objects.actor.actor import Actor
from app.helpers.unique_name import generate_unique_name

V = TypeVar("V", bound=Actor)

class ActorsCollection(CollectionBase[str, V], Generic[V]):
    def __init__(self, items: dict[str, V] | None = None):
        super().__init__(items or {})

    def possessed_by_player(self) -> Self:
        return type(self)(self.filter(lambda a: a.player))

    def get_active_actors(self) -> Self:
        return type(self)(self.filter(lambda a: a.active))

    def subtract_actors(self, other: Self) -> Self:
        if not other:
            return self
        return type(self)({k: v for k, v in self.data.items() if k not in other})

    def add(self, actor: V) -> None:
        if actor.name and actor.name not in self.data:
            name = actor.name
        else:
            name = generate_unique_name(set(self.data.keys()))
            actor.name = name

        self.data[name] = actor

