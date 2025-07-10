from typing import TypeVar, Generic, Self

from appv2.core.collection_base import CollectionBase
from appv2.core.unique_name import generate_unique_name
from appv2.protocols.objects.actor_protocol import ActorProtocol

V = TypeVar("V", bound=ActorProtocol)

class ActorsCollection(CollectionBase[str, V], Generic[V]):
    def __init__(self, items: dict[str, V] | None = None):
        super().__init__(items or {})

    def get_active_actors(self) -> Self:
        return type(self)(self.filter(lambda a: a.is_active and not a.is_deleted))

    def __check_and_delete(self, name: str) -> bool:
        if name in self.data and self.data[name].is_deleted:
            del self.data[name]
            return True
        return False

    def clean(self) -> None:
        to_remove = [name for name, actor in self.data.items() if actor.is_deleted]
        for name in to_remove:
            del self.data[name]

    def __contains__(self, name: str) -> bool:
        return not self.__check_and_delete(name) and name in self.data

    def __getitem__(self, name: str):
        if self.__check_and_delete(name):
            raise KeyError(f"Actor '{name}' was deleted.")

        return super().__getitem__(name)

    # For example, what if name is not equal to actor.name
    def __setitem__(self, name: str, actor: ActorProtocol):
        if not actor.is_deleted:
            super().__setitem__(name, actor)

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

        super().__setitem__(name, actor)

