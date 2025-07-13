# 🧠 Actor Lifecycle & Registry Ownership Strategy

This document outlines the recommended strategy for managing actors and lifecycle cleanup using the `Supervisor` and `actors_registry`. This pattern enables robust, low-coupling architecture inspired by ECS and real-world game engine designs.

## Table of Contents

1. [Actor Lifecycle & Registry Ownership Strategy](#-actor-lifecycle--registry-ownership-strategy)
2. [Principle 1: Only the Orchestrator Needs `actors_registry`](#-principle-1-only-the-orchestrator-needs-actors_registry)
3. [Principle 2: Orchestrator Handles Actor Deletion](#-principle-2-orchestrator-handles-actor-deletion)
4. [Problem: Zombie References](#-problem-zombie-references)
5. [Safe Zombie Cleanup Strategy](#-safe-zombie-cleanup-strategy)
   - [Passive Cleanup on Access](#-passive-cleanup-on-access)
6. [Orchestrator Implementation](#-orchestrator-implementation)
   - [Orchestrator — Key Responsibilities](#-orchestrator--key-responsibilities)
   - [1. Control Pending Actions](#1-control-pending-actions)
   - [2. Actor Deletion Lifecycle](#2-actor-deletion-lifecycle)
   - [3. Puppeteer Registration](#3-puppeteer-registration)
   - [4. Receive Input Log Records](#4-receive-input-log-records)
   - [5. Access to Global State](#5-access-to-global-state)
   - [Suggested File Layout](#-suggested-file-layout)

---

## ✅ Principle 1: Only the Orchestrator Needs `actors_registry`

- All other systems (Grid, Input, Pipeline, Behaviours) work with actor **references** already handed to them.
- They do **not** need global access to the registry.
- ✅ This simplifies dependencies and prevents circular imports.

---

## ✅ Principle 2: Orchestrator Handles Actor Deletion

The Supervisor is responsible for:

- Marking the actor as `.is_deleted = True`
- Removing it from `actors_registry`
- Letting all other systems clean up lazily when they interact with the deleted actor

✅ This mirrors standard patterns in **Unreal, Unity, and ECS-based engines**.

### Benefits:
- Predictable invalidation
- Centralized control
- No race conditions or hard crashes from dangling references

---

## 🧠 Problem: Zombie References

> "What if something holds a reference to a deleted actor and never uses it again?"

These are "zombies":

- Actor no longer participates in the game
- Still exists in:
  - `Cell._holders`
  - `Puppeteer.puppet`
  - `input_registry.subscribers`
  - `command_pipeline.queue`

---

## ✅ Safe Zombie Cleanup Strategy

### 🔁 Passive Cleanup on Access

Each system checks `.is_deleted` before using an actor:

```python
if actor.is_deleted:
    self._holders.discard(actor)
    return
```

---

## 🎯 Orchestrator Implementation

### ✅ Orchestrator — Key Responsibilities

#### 🧠 Message-Driven Actor

```python
class Orchestrator(Actor):
    ...
```

Allows:
- Behaviours to react to messages like `REQUEST_DELETE`, `KEY_PRESSED`, etc.
- Fully event-driven design

### 1. Control Pending Actions

```python
def tick():
    for actor in self.actors.get_active_actors():
        if not actor.should_retain_pending_actions():  # or via message
            actor.pending_actions.clear()
```

✅ Might even be extracted into a `PendingActionManager` behaviour

### 2. Actor Deletion Lifecycle

Actors send:

```python
Message(
    sender=actor.name,
    body=MessageBody(message_type=MessageTypes.REQUEST_DELETE, payload=Reason(...))
)
```

Orchestrator handles via a `LifecycleManagerBehaviour`:
- Marks actor `.is_deleted = True`
- Optionally calls `actor.finalize()`
- Removes from registry or queues

✅ Fully controlled, safe deletion

### 3. Puppeteer Registration

On startup or actor creation, Orchestrator can:

```python
input_router.register(puppeteer)
```

Or send an event to the input handler via:

```python
Message(..., message_type=REGISTER_INPUT_HANDLER, ...)
```

✅ Keeps input system modular and replaceable

### 4. Receive Input Log Records

Orchestrator gets messages like:

```python
Message(sender="application", body=KeyPressEventLogRecord(dt=..., key=..., down=...))
```

Handled by `OrchestratorInputBehaviour`, which:
- Parses log entries
- Converts to `KEY_DOWN` / `KEY_UP`
- Sends messages to corresponding puppeteer(s)

✅ Abstracts input source from simulation logic

### 5. Access to Global State

At init:

```python
self.actors: ActorCollection = self.level_factory.levels["level1"].actors
```

✅ Holds the truth, no need for globals

### 🧱 Suggested File Layout

```
orchestrator/
├── orchestrator.py                   # The Actor
├── behaviours/
│   ├── input_handler.py            # From KeyPressEventLogRecord
│   ├── pending_manager.py          # Clears actor pending_actions
│   └── lifecycle_manager.py        # Handles REQUEST_DELETE, etc.
