from collections import UserDict
from dataclasses import dataclass
from typing import Callable

from ui.actors.actions import Actions


@dataclass
class Action:
    function: Callable[[], None]
    repeat_delta: int = -1

    def __call__(self):
        self.function()


class Controls(UserDict[int, Action]):
    def __init__(self, actions: Actions):
        super().__init__()
        self.actions = actions
        pass

    def action(self, key: str):
        pass

