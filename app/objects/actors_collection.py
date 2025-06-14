from app.helpers.collection_base import CollectionBase
from app.objects.actor.actor import Actor
from typing import TypeVar, Generic

T = TypeVar("T", bound=Actor)

class ActorsCollection(CollectionBase[T], Generic[T]):
    def __init__(self, items: dict[str, Actor] | None = None):
        super().__init__(items or {})

    def get_active_actors(self) -> "ActorsCollection":
        return ActorsCollection(self.filter(lambda a: a.active))
