import importlib

from app.config import Behaviours
from appv2.protocols.behaviours.behaviour_protocol import BehaviourProtocol


class BehaviourRegistry:
    modulePath = "app.behaviours"

    def __init__(self):
        self.registry: dict[Behaviours, BehaviourProtocol] = {}

    def load(self, behaviour: Behaviours):
        module_path, class_name = behaviour.value.rsplit(".", 1)
        full_path = f"{self.modulePath}{module_path}"

        try:
            module = importlib.import_module(full_path)
            cls = getattr(module, class_name, None)

            self.registry[behaviour] = cls
        except Exception as e:
            raise ImportError(f"Failed to load behaviour {behaviour}: {e}") from e

    def get(self, behaviour: Behaviours) -> BehaviourProtocol:
        if behaviour not in self.registry:
            self.load(behaviour)

        return self.registry.get(behaviour)

_registry_instance: BehaviourRegistry | None = None

def get_registry() -> BehaviourRegistry:
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = BehaviourRegistry()
    return _registry_instance

