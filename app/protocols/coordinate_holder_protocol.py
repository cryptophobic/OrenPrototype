from typing import Protocol, runtime_checkable
from abc import ABC, abstractmethod

from ..helpers.vectors import Vec2
from ..objects.actor.body import Body
from ..objects.actor.shape import Shape
from .actor_protocol import ActorProtocol


@runtime_checkable
class CoordinateHolderProtocol(ActorProtocol, Protocol):
    """Protocol for objects that have coordinates and can be moved."""
    
    body: Body
    shape: Shape
    coordinates: Vec2
    
    def blocks(self, other: 'CoordinateHolderProtocol') -> bool:
        """Check if this object blocks another object."""
        ...
    
    def overlaps(self, other: 'CoordinateHolderProtocol') -> bool:
        """Check if this object overlaps with another object."""
        ...


@runtime_checkable
class UnitProtocol(CoordinateHolderProtocol, Protocol):
    """Protocol for units that have stats and can perform actions."""
    
    stats: 'StatsProtocol'


@runtime_checkable
class StaticObjectProtocol(CoordinateHolderProtocol, Protocol):
    """Protocol for static objects with physical properties."""
    
    height: int
    weight: int


@runtime_checkable
class StatsProtocol(Protocol):
    """Protocol for unit statistics."""
    
    STR: int
    DEX: int
    CON: int
    INT: int
    WIS: int
    CHA: int
    HP: int
    initiative: int


class CoordinateHolderInterface(ABC):
    """Abstract base class for coordinate holders."""
    
    @abstractmethod
    def blocks(self, other: 'CoordinateHolderInterface') -> bool:
        pass
    
    @abstractmethod
    def overlaps(self, other: 'CoordinateHolderInterface') -> bool:
        pass