# 🧠 Actor Lifecycle & Registry Ownership Strategy

This document outlines the recommended strategy for managing actors and lifecycle cleanup using the `Supervisor` and `actors_registry`. This pattern enables robust, low-coupling architecture inspired by ECS and real-world game engine designs.

---

## ✅ Principle 1: Only the Supervisor Needs `actors_registry`

- All other systems (Grid, Input, Pipeline, Behaviours) work with actor **references** already handed to them.
- They do **not** need global access to the registry.
- ✅ This simplifies dependencies and prevents circular imports.

---

## ✅ Principle 2: Supervisor Handles Actor Deletion

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
