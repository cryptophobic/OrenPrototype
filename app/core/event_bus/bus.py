import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Any

from app.core.event_bus.events import Events
from app.protocols.objects.component_protocol import ComponentProtocol


class Strategy(Enum):
    AtMostOnce = 1
    AtLeastOnce = 2
    FirstWin = 3

@dataclass(frozen=True, slots=True)
class Envelope:
    event: Events
    payload: Any
    strategy: Strategy
    route: str = ''
    ttl_s: float | None = 6.0
    ts: float = field(default_factory=time.time)

@dataclass(frozen=True, slots=True)
class Subscription:
    callback: Callable[[Any], None]
    route: str = ''  # empty = subscribe to all routes

MAX_BACKLOG = 1000

class EventBus:

    def __init__(self):
        self._subs: dict[Events, list[Subscription]] = defaultdict(list)
        self._backlog: dict[Events, deque[Envelope]] = defaultdict(lambda: deque(maxlen=MAX_BACKLOG))
        self._retained: dict[tuple[Events, str | None], Envelope] = {}

    def subscribe(self, ev: Events, cb: Callable[[Any], None], route: str = ''):
        """
        Subscribe to an event with optional route filtering.
        - route='': subscribes to all routes (broadcast and targeted)
        - route='comp_123': only receives events routed to 'comp_123'
        """
        sub = Subscription(callback=cb, route=route)
        self._subs[ev].append(sub)
        self._drain_backlog(ev, route)

    def subscribe_component(self, component: ComponentProtocol, ev: Events, cb: Callable[[Any], None]):
        """
        Convenience method: subscribe using a component's ID as the route.
        Automatically uses component.id as the route filter.
        """
        self.subscribe(ev, cb, route=component.id)

    def unsubscribe_component(self, component: ComponentProtocol, ev: Events, cb: Callable[[Any], None]) -> bool:
        """
        Convenience method: unsubscribe using a component's ID as the route.
        Automatically uses component.id as the route filter.
        """
        return self.unsubscribe(ev, cb, route=component.id)

    def unsubscribe(self, ev: Events, cb: Callable[[Any], None], route: str | None = None) -> bool:
        """
        Remove a callback for a single event. Returns True if it was removed.
        - If route is None: removes all subscriptions with this callback
        - If route is specified: only removes subscriptions matching both callback and route
        """
        subs = self._subs.get(ev)
        if not subs:
            return False

        removed = False
        if route is None:
            # remove all subscriptions with this callback
            original_len = len(subs)
            subs[:] = [s for s in subs if s.callback is not cb]
            removed = len(subs) < original_len
        else:
            # remove only subscriptions matching both callback and route
            original_len = len(subs)
            subs[:] = [s for s in subs if not (s.callback is cb and s.route == route)]
            removed = len(subs) < original_len

        # tidy up empty lists to keep dict small
        if not subs:
            self._subs.pop(ev, None)
        return removed

    def unsubscribe_all(self, cb: Callable[[Any], None]) -> int:
        """Remove a callback from all events. Returns the number of removals."""
        removed = 0
        empty_keys = []
        for ev, subs in self._subs.items():
            # remove all occurrences (defensive)
            count_before = len(subs)
            subs[:] = [s for s in subs if s.callback is not cb]
            removed += count_before - len(subs)
            if not subs:
                empty_keys.append(ev)
        for ev in empty_keys:
            self._subs.pop(ev, None)
        return removed

    def emit(self,
             ev: Events,
             payload: Any,
             strategy: Strategy = Strategy.AtMostOnce,
             route: str = '',):
        """
        Emit an event with optional routing.
        - route='': broadcasts to all subscribers
        - route='comp_123': only delivered to subscribers listening to 'comp_123' or ''
        """
        env = Envelope(ev, payload, strategy, route)

        subs = self._subs.get(ev, [])
        # filter subscribers that match the route
        matching_subs = self._filter_matching_subs(subs, env.route)

        if not matching_subs:
            if strategy is Strategy.AtMostOnce:
                return
            # buffer for later delivery
            self._backlog[ev].append(env)
            return

        # deliver now
        self._deliver_to_matching(matching_subs, env)

    # ---- internals ----
    @staticmethod
    def _route_matches(sub_route: str, emit_route: str) -> bool:
        """
        Check if a subscription route matches an emitted route.
        - sub_route='': matches all emitted routes (broadcast listener)
        - emit_route='': broadcasts to all subscriptions
        - otherwise: exact match required
        """
        if sub_route == '':
            return True  # the subscriber listens to everything
        if emit_route == '':
            return True  # broadcast event reaches all
        return sub_route == emit_route

    @staticmethod
    def _filter_matching_subs(subs: list[Subscription], emit_route: str) -> list[Subscription]:
        """Return only subscriptions that match the emitted route."""
        return [s for s in subs if EventBus._route_matches(s.route, emit_route)]

    @staticmethod
    def _deliver_to_matching(subs: list[Subscription], env: Envelope):
        """Deliver envelope to matching subscriptions."""
        for sub in list(subs):
            sub.callback(env.payload)
            if env.strategy is Strategy.FirstWin:
                return

    def _drain_backlog(self, ev: Events, new_sub_route: str = ''):
        """Drain the backlog for a specific event, filtering by the new subscription's route."""
        if not self._subs.get(ev):
            return
        q = self._backlog[ev]
        # single-pass drain snapshot to avoid infinite loops
        n = len(q)
        for _ in range(n):
            env = q.popleft()
            if env.ttl_s is not None and time.time() - env.ts > env.ttl_s:
                continue  # expired
            # only deliver if the new subscription had matched
            if self._route_matches(new_sub_route, env.route):
                matching_subs = self._filter_matching_subs(self._subs[ev], env.route)
                self._deliver_to_matching(matching_subs, env)


# SINGLE shared bus
bus = EventBus()
