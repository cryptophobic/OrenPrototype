from collections import UserDict

from actor_protocol import ActorProtocol
from appv2.engine.message_broker.types import KeyBinding


class Controls(UserDict[int, KeyBinding]):
    pass

class Puppeteer(ActorProtocol):
    def __init__(self, puppet: ActorProtocol, controls: Controls, name: str = None):
        super().__init__(name)

        self.puppet = puppet
        self.controls = controls
