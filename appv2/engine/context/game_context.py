from app.engine.message_broker.message_broker import MessageBroker
from app.registry.actor_registry import ActorRegistry

class GameContext:
    def __init__(self):
        self.actor_registry = ActorRegistry()
        self.message_broker = MessageBroker(actor_registry=self.actor_registry)
        self.frame_number = 0

    def tick(self) -> None:
        self.frame_number += 1
