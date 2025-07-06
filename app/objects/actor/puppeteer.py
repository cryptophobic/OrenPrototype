from collections import UserDict
from dataclasses import dataclass

from .actor import Actor
from ...bus.message_broker.types import MessageBody

@dataclass
class KeyBinding:
    key_down: MessageBody
    key_up: MessageBody = None

class Controls(UserDict[int, KeyBinding]):
    pass

class Puppeteer(Actor):
    def __init__(self, puppet: Actor, controls: Controls, name: str = None):
        super().__init__(name)

        self.puppet = puppet
        self.controls = controls
