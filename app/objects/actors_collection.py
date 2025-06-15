from app.helpers.collection_base import CollectionBase
from app.helpers.unique_name import generate_unique_name
from app.objects.actor.actor import Actor
from typing import TypeVar, Generic

T = TypeVar("T", bound=Actor)

class ActorsCollection(CollectionBase[T], Generic[T]):
    def __init__(self, items: dict[str, Actor] | None = None):
        super().__init__(items or {})

    def possessed_by_player(self) -> CollectionBase[T]:
        return CollectionBase[T](self.filter(lambda a: a.player))

    def get_active_actors(self) -> CollectionBase[T]:
        return CollectionBase[T](self.filter(lambda a: a.active))

    def subtract_actors(self, other: CollectionBase[T]) -> CollectionBase[T]:
        if not other:
            return self

        return CollectionBase[T]({k: v for k, v in self.data.items() if k not in other})

    def add(self, actor: T):
        if actor.name and actor.name not in self.data:
            name = actor.name
        else:
            name = generate_unique_name(set(self.data.keys()))
            actor.name = name

        self.data[name] = actor

