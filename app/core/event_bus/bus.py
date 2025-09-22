import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Any

from app.core.event_bus.events import Events

class Strategy(Enum):
    AtMostOnce = 1
    AtLeastOnce = 2
    FirstWin = 3

@dataclass(frozen=True, slots=True)
class Envelope:
    event: Events
    payload: Any
    strategy: Strategy
    ttl_s: float | None = 6.0
    ts: float = field(default_factory=time.time)

MAX_BACKLOG = 1000

class EventBus:

    def __init__(self):
        self._subs: dict[Events, list[Callable[[Any], None]]] = defaultdict(list)
        self._backlog: dict[Events, deque[Envelope]] = defaultdict(lambda: deque(maxlen=MAX_BACKLOG))
        self._retained: dict[tuple[Events, str | None], Envelope] = {}

    def subscribe(self, ev: Events, cb: Callable[[Any], None]):
        self._subs[ev].append(cb)
        self._drain_backlog(ev)

    def unsubscribe(self, ev: Events, cb: Callable[[Any], None]) -> bool:
        """Remove a callback for a single event. Returns True if it was removed."""
        subs = self._subs.get(ev)
        if not subs:
            return False
        try:
            subs.remove(cb)
        except ValueError:
            return False
        # tidy up empty lists to keep dict small
        if not subs:
            self._subs.pop(ev, None)
        return True

    def unsubscribe_all(self, cb: Callable[[Any], None]) -> int:
        """Remove a callback from all events. Returns the number of removals."""
        removed = 0
        empty_keys = []
        for ev, subs in self._subs.items():
            # remove all occurrences (defensive)
            count_before = len(subs)
            subs[:] = [s for s in subs if s is not cb]
            removed += count_before - len(subs)
            if not subs:
                empty_keys.append(ev)
        for ev in empty_keys:
            self._subs.pop(ev, None)
        return removed

    def emit(self, ev: Events, payload: Any, strategy: Strategy = Strategy.AtMostOnce):
        env = Envelope(ev, payload, strategy)

        subs = self._subs.get(ev, [])
        if not subs:
            if strategy is Strategy.AtMostOnce:
                return
            # buffer for later delivery
            self._backlog[ev].append(env)
            return

        # deliver now
        self._deliver_to_all(subs, env)

    # ---- internals ----
    @staticmethod
    def _deliver_to_all(subs: list[Callable], env: Envelope):
        for cb in list(subs):
            cb(env.payload)
            if env.strategy is Strategy.FirstWin:
                return

    def _drain_backlog(self, ev: Events):
        if not self._subs.get(ev):
            return
        q = self._backlog[ev]
        # single-pass drain snapshot to avoid infinite loops
        n = len(q)
        for _ in range(n):
            env = q.popleft()
            if time.time() - env.ts > env.ttl_s:
                continue  # expired
            self._deliver_to_all(self._subs[ev], env)


# SINGLE shared bus
bus = EventBus()
