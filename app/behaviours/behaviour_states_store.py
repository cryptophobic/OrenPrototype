from dataclasses import replace, is_dataclass
from contextlib import contextmanager
from typing import Any, Dict, Iterator

from app.config import Behaviours


class BehaviourStateStore:
    def __init__(self):
        self._map: Dict[Behaviours, Any] = {}

    def get(self, key: Behaviours):
        return self._map.get(key)

    def get_copy(self, key: Behaviours, default: type):
        state = self._map.get(key, default())
        assert is_dataclass(state), "State must be a dataclass"
        return replace(state)

    def set(self, key: Behaviours, value: Any) -> None:
        self._map[key] = value

    @contextmanager
    def mutate(self, key: Behaviours) -> Iterator[Any]:
        """Copy → yield draft → commit if changed."""
        original = self._map[key]
        assert is_dataclass(original)
        draft = replace(original)
        yield draft
        if draft != original:
            self._map[key] = draft
