from typing import Protocol


class ComponentProtocol(Protocol):
    @property
    def id(self) -> str:...
