from collections import UserDict
from typing import Type, TypeVar, cast

from app.helpers.unique_name import generate_unique_name
from app.protocols.actor_protocol import ActorProtocol
from app.protocols.coordinate_holder_protocol import CoordinateHolderProtocol
from appv2.protocols.unit_protocol import UnitProtocol
from appv2.protocols.static_object_protocol import StaticObjectProtocol
from appv2.protocols.puppeteer_protocol import PuppeteerProtocol

T = TypeVar("T", bound=ActorProtocol)

class ActorRegistry(UserDict[str, ActorProtocol]):
    def add(self, actor: ActorProtocol, preferred_name: str = None) -> str:
        name = preferred_name or actor.name or generate_unique_name(set(self.data.keys()))
        actor.name = name
        self.data[name] = actor
        return name

    def remove(self, name: str) -> bool:
        return self.data.pop(name, None) is not None

    def get_by_type(self, cls: Type[T]) -> dict[str, T]:
        return {
            name: cast(T, actor)
            for name, actor in self.data.items()
            if isinstance(actor, cls)
        }

    def all(self) -> list[ActorProtocol]:
        return list(self.data.values())

    def get(self, name: str) -> ActorProtocol:
        return self.data[name]

    def get_units(self) -> list[UnitProtocol]:
        return list(self.get_by_type(UnitProtocol).values())

    def get_static_objects(self) -> list[StaticObjectProtocol]:
        return list(self.get_by_type(StaticObjectProtocol).values())

    def get_coordinate_holders(self) -> list[CoordinateHolderProtocol]:
        return list(self.get_by_type(CoordinateHolderProtocol).values())

    def get_puppeteers(self) -> list[PuppeteerProtocol]:
        return list(self.get_by_type(PuppeteerProtocol).values())
