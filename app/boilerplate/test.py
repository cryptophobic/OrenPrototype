from __future__ import annotations
from dataclasses import fields, dataclass, asdict, is_dataclass

from contextlib import contextmanager
from enum import Enum, auto
from typing import Any, Dict, Iterator

from app.behaviours.types import SimpleVec2Bool
from app.core.vectors import CustomVec2f


# --- Your behaviour keys ---
class Behaviours(Enum):
    BUFFERED_MOVER = auto()
    # add more behaviours here...

# --- Example frozen state ---
@dataclass(frozen=True, slots=True)
class BufferedMoverState:
    moving_buffer: CustomVec2f
    intent_velocity: CustomVec2f
    intent_velocity_normalised: CustomVec2f
    clear_velocity: SimpleVec2Bool

# --- Draft proxy ---
class _DraftProxy:
    def __init__(self, cls: type, data: Dict[str, Any]):
        # real attributes (won't hit __getattr__/__setattr__)
        super().__setattr__("_DraftProxy__cls", cls)
        super().__setattr__("_DraftProxy__data", data)
        allowed = {f.name for f in fields(cls)}  # dataclass fields
        super().__setattr__("_DraftProxy__allowed", allowed)
        self.__cls = cls
        self.__data = data

    def __getattr__(self, name: str) -> Any:
        try: return self.__data[name]
        except KeyError: raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_" + _DraftProxy.__name__ + "__"):
            return super().__setattr__(name, value)
        self.__data[name] = value

    def freeze(self):
        return self.__cls(**self.__data)

# --- Store keyed by Behaviours ---
class BehaviourStateStore:
    def __init__(self):
        self._map: Dict[Behaviours, Any] = {}

    def get(self, key: Behaviours):
        return self._map.get(key)

    def set(self, key: Behaviours, value: Any) -> None:
        self._map[key] = value

    @contextmanager
    def edit(self, key: Behaviours) -> Iterator[_DraftProxy]:
        current = self._map.get(key)
        if current is None:
            raise KeyError(f"No state for {key!r}")
        if not is_dataclass(current):
            raise TypeError("State must be a dataclass instance")

        draft_dict = asdict(current)              # type-narrowed above
        draft = _DraftProxy(type(current), draft_dict)
        yield draft                                # user mutates draft
        self._map[key] = draft.freeze()            # commit


def test():
    store = BehaviourStateStore()

    store.set(
        Behaviours.BUFFERED_MOVER,
        BufferedMoverState(
            moving_buffer=CustomVec2f.zero(),
            intent_velocity=CustomVec2f.zero(),
            intent_velocity_normalised=CustomVec2f.zero(),
            clear_velocity=SimpleVec2Bool(False, False),
        ),
    )

    with store.edit(Behaviours.BUFFERED_MOVER) as s:
        s.moving_buffer = s.moving_buffer.with_index(CustomVec2f.x, 1.0)

    state = store.get(Behaviours.BUFFERED_MOVER)
