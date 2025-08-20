from dataclasses import asdict, is_dataclass
from contextlib import contextmanager
from typing import Any, Dict, Iterator



# --- Draft proxy ---
class _DraftProxy:
    def __init__(self, cls: type, data: Dict[str, Any]):
        self.__cls = cls
        self.__data = data

    def __getattr__(self, name: str) -> Any:
        try: return self.__data[name]
        except KeyError: raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_" + _DraftProxy.__name__ + "__"):
            return super().__setattr__(name, value)
        self.__data[name] = value
        return None

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
