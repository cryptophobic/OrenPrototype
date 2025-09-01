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
    ttl_s: float | None = 5.0
    ts: float = field(default_factory=time.time)


class EventBus:

    def __init__(self):
        self._subs: dict[Events, list[Callable[[Any], None]]] = defaultdict(list)
        self._backlog: dict[Events, deque[Envelope]] = defaultdict(deque)
        self._retained: dict[tuple[Events, str | None], Envelope] = {}

    def subscribe(self, ev: Events, cb: Callable[[Any], None]):
        self._subs[ev].append(cb)
        self._drain_backlog(ev)

    def emit(self, ev: Events, payload: Any,
             strategy: Strategy = Strategy.AtMostOnce,
             ttl_s: float | None = None):
        env = Envelope(ev, payload, strategy, ttl_s or 5.0)

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
    def _deliver_to_all(self, subs: list[Callable], env: Envelope):
        for cb in list(subs):
            self._deliver_env(cb, env)
            if env.strategy is Strategy.FirstWin:
                return

    def _deliver_env(self, cb: Callable, env: Envelope):
        try:
            cb(env.payload)
        except Exception:
            if env.strategy is Strategy.AtLeastOnce or env.strategy is Strategy.FirstWin:
                # requeue if TTL not exceeded
                if time.time() - env.ts < (env.ttl_s or 5.0):
                    self._backlog[env.event].append(env)
            # swallow to avoid breaking other subscribers

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
            # if delivery failed for some, _deliver_env may requeue


# SINGLE shared bus
bus = EventBus()
