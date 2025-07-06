import importlib
import inspect
from typing import TYPE_CHECKING

from app.config import Behaviours

if TYPE_CHECKING:
    from app.behaviours.behaviour import Behaviour


class BehaviourRegistry:
    modulePath = "app.behaviours"

    def __init__(self):
        self.registry: dict[Behaviours, type['Behaviour']] = {}

    def load(self, behaviour: Behaviours):
        module_path, class_name = behaviour.value.rsplit(".", 1)
        full_path = f"{self.modulePath}{module_path}"

        try:
            module = importlib.import_module(full_path)
            cls = getattr(module, class_name, None)

            # Import Behaviour at runtime to avoid circular imports
            from app.behaviours.behaviour import Behaviour
            if inspect.isclass(cls) and issubclass(cls, Behaviour):
                self.registry[behaviour] = cls
            else:
                raise TypeError(f"{class_name} is not a valid Behaviour class")
        except Exception as e:
            raise ImportError(f"Failed to load behaviour {behaviour}: {e}") from e

    def get(self, behaviour: Behaviours) -> type['Behaviour']:
        if behaviour not in self.registry:
            self.load(behaviour)

        return self.registry.get(behaviour)

# behaviour_registry.py
_registry_instance: BehaviourRegistry | None = None

def get_registry() -> BehaviourRegistry:
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = BehaviourRegistry()
    return _registry_instance
