from typing import TypeVar, Generic, Self, Iterator, Callable, Type, cast

from app.config import Behaviours
from app.core.collection_base import CollectionBase
from app.core.unique_name import generate_unique_name
from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol

V = TypeVar("V", bound=ActorProtocol)
T = TypeVar("T", bound=ActorProtocol)
C = TypeVar("C", bound="ActorCollection")

class ActorCollection(CollectionBase[str, V], Generic[V], ActorCollectionProtocol[V]):
    def get_active_actors(self) -> Self:
        return self.filter(lambda a: a.is_active)

    def get_pending_actors(self) -> Self:
        return self.filter(lambda a: a.pending_actions)

    def get_behave_as_this(self, behaviour: Behaviours, first = False) -> Self | V:
        res = self.filter(lambda a: a.is_behave_as_this(behaviour))
        return next(iter(res), None) if first else res

    def get_behave_as_them(self, behaviours: list[Behaviours], first = False) -> Self | V:
        res = self.filter(lambda a: a.is_behave_as_them(behaviours))
        return next(iter(res), None) if first else res

    def get_behave_as_any(self, behaviours: list[Behaviours], first = False) -> Self | V:
        res = self.filter(lambda a: a.is_behave_as_any(behaviours))
        return next(iter(res), None) if first else res

    def get_deleted_actors(self) -> Self:
        return self.__class__({k: v for k, v in self.items.items() if v.is_deleted})

    def __iter__(self) -> Iterator[V]:
        return iter(actor for actor in self.items.values() if not actor.is_deleted)
    
    def __len__(self) -> int:
        return sum(1 for actor in self.items.values() if not actor.is_deleted)

    def filter(self, predicate: Callable[[V], bool]) -> Self:
        return self.__class__({
            k: v for k, v in self.items.items()
            if not v.is_deleted and predicate(v)
        })

    def get_by_type(
            self,
            cls: Type[T],
            collection_type: Type[C] = None
    ) -> C:
        matched = {
            name: cast(T, actor)
            for name, actor in self.items.items()
            if isinstance(actor, cls) and not actor.is_deleted
        }
        result_cls = collection_type or self.__class__
        return result_cls(matched)  # type: ignore

    def __contains__(self, name: str) -> bool:
        return name in self.items and not self.items[name].is_deleted

    def clean(self) -> None:
        for name, actor in self.raw_items().items():
            if actor.is_deleted:
                del self.items[name]

    def get(self, key: str) -> V | None:
        actor = self.raw_items().get(key)
        if actor is None or actor.is_deleted:
            return None
        return actor

    def add(self, actor: V) -> None:
        if actor.name and actor.name not in self.items:
            name = actor.name
        else:
            name = generate_unique_name(set(self.items.keys()))
            actor.name = name

        self.items[name] = actor

