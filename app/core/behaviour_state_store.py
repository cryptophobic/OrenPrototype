from dataclasses import asdict, is_dataclass
from contextlib import contextmanager
from typing import Any, Dict, Generic, Type, TypeVar

from app.behaviours.types import BehaviourStates, BehaviourState
from app.config import Behaviours

class _DraftProxy:
    def __init__(self, cls: BehaviourState, data: Dict[str, Any]):
        self.__cls = cls
        self.__data = data

    def __getattr__(self, name: str) -> Any:
        try:
            return self.__data[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_" + _DraftProxy.__name__ + "__"):
            return super().__setattr__(name, value)
        self.__data[name] = value
        return None

    def freeze(self) -> BehaviourState:
        # Reconstruct a fresh frozen dataclass instance
        return self.__cls(**self.__data)

class BehaviourStateStore(Generic[S]):
    def __init__(self):
        self._map: BehaviourStates = {}

    def get(self, cls: Behaviours) -> S | None:
        return self._map.get(cls)

    def set(self, cls: Behaviours, value: BehaviourState) -> None:
        self._map[cls] = value

    @contextmanager
    def edit(self, cls: Type[S]):
        current: S | None = self._map.get(cls)
        if current is None:
            raise KeyError(f"No state for {cls.__name__}")
        if not is_dataclass(current):
            raise TypeError("State must be a dataclass")

        # Start a mutable draft dict from the frozen instance
        draft_dict = asdict(current)  # shallow values are your immutables; safe
        draft = _DraftProxy(cls, draft_dict)
        yield draft  # user mutates draft attr-by-attr

        # Commit
        new_state = draft.freeze()
        self._map[cls] = new_state
