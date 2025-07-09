from typing import TypeVar, Generic, Self, Type

from appv2.core.collection_base import CollectionBase
from appv2.core.unique_name import generate_unique_name
from appv2.protocols.objects.actor_protocol import ActorProtocol

V = TypeVar("V", bound=ActorProtocol)

class ActorsCollection(CollectionBase[str, V], Generic[V]):
    def __init__(self, items: dict[str, V] | None = None):
        super().__init__(items or {})

    def get_by_classname(self, cls: Type[V]) -> dict[str, V]:
        return {
            name: actor for name, actor in self.data.items()
            if isinstance(actor, cls)
        }

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

