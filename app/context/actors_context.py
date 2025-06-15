from collections import UserDict
from typing import TypeVar, Type

from ..helpers.unique_name import generate_unique_name
from ..objects.actor.actor import Actor
from ..objects.actor.coordinate_holder import CoordinateHolder
from ..objects.actor.static_object import StaticObject
from ..objects.actor.unit import Unit
from ..objects.actors_collection import ActorsCollection
from ..objects.coordinate_holders_collection import CoordinateHoldersCollection
from ..objects.static_objects_collection import StaticObjectsCollection
from ..objects.units_collection import UnitsCollection

T = TypeVar("T", bound=Actor)

class ActorsContext(UserDict[str, Actor]):
    def __init__(self):
        super().__init__()

    def __get_by_type(self, cls: Type[T]) -> dict[str, T]:
        return {
            name: actor for name, actor in self.data.items()
            if isinstance(actor, cls)
        }

    def get_coordinate_holders(self) -> CoordinateHoldersCollection:
        return CoordinateHoldersCollection(self.__get_by_type(CoordinateHolder)).get_active_actors()

    def get_static_objects(self) -> StaticObjectsCollection:
        return StaticObjectsCollection(self.__get_by_type(StaticObject)).get_active_actors()

    def get_units(self) -> UnitsCollection:
        return UnitsCollection(self.__get_by_type(Unit)).get_active_actors()

    def get_actors(self) -> ActorsCollection:
        return ActorsCollection(self.data.copy()).get_active_actors()

    def add_actor(self, actor) -> str:
        """Add an actor with unique name generation if needed"""
        if actor.name and actor.name not in self.data:
            name = actor.name
        else:
            name = generate_unique_name(set(self.data.keys()))
            actor.name = name
        
        self.data[name] = actor
        return name

    def remove_actor(self, actor_name: str) -> bool:
        """Remove an actor by name"""
        if actor_name in self.data:
            del self.data[actor_name]
            return True
        return False