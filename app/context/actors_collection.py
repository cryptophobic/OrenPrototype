from collections import UserDict
from typing import List
import time

from app.objects.actor.actor import Actor


class ActorsCollection(UserDict[str, Actor]):
    def __init__(self):
        super().__init__()

    def add_actor(self, actor) -> str:
        """Add an actor with unique name generation if needed"""
        if actor.name and actor.name not in self.data:
            name = actor.name
        else:
            name = self.generate_unique_name()
            actor.name = name
        
        self.data[name] = actor
        return name

    def generate_unique_name(self) -> str:
        """Generate a unique actor name with timestamp fallback"""
        try:
            import petname
            base_name = petname.Generate(2, separator="-")
        except ImportError:
            base_name = f"actor-{len(self.data)}"
        
        timestamp = int(time.time() * 1000) % 10000
        name = f"{base_name}-{timestamp}"
        
        if name in self.data:
            counter = timestamp + 1
            while f"{base_name}-{counter}" in self.data:
                counter += 1
            name = f"{base_name}-{counter}"
        
        return name

    def get_active_actors(self) -> List:
        """Get all active actors"""
        return [actor for actor in self.data.values() if getattr(actor, 'active', True)]

    def get_dirty_actors(self) -> List:
        """Get all actors marked as dirty"""
        return [actor for actor in self.data.values() if getattr(actor, 'dirty', False)]

    def remove_actor(self, actor_name: str) -> bool:
        """Remove an actor by name"""
        if actor_name in self.data:
            del self.data[actor_name]
            return True
        return False