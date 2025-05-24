from collections import UserDict
from dataclasses import dataclass
from typing import Callable
from ui.actors.actor import Actor

@dataclass
class Action:
    function: Callable[[], None]
    repeat_delta: int = -1

    def __call__(self):
        self.function()


class Controls(UserDict[int, Action]):
    def __init__(self, actor: Actor):
        super().__init__()
        self.actor = actor
        pass

    def action(self, key: str):
        pass

