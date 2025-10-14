# Animation System Refactoring Discussion

## Current Problem

The `Shape` class currently mixes visual data with behavioral state:
- `current_animation: UnitStates` - This is really **state** (what the unit is doing), not animation data
- `direction: Directions` - Facing direction for rendering
- `animations: AnimationCollection` - Actual texture/animation data

**Location**: `app/core/geometry/shape.py:11`

## Current Flow

1. `BufferedMover` behavior calculates movement (`app/behaviours/moveable/buffered_mover.py:36`)
2. Updates `coordinate_holder.shape.current_animation` and `coordinate_holder.shape.direction`
3. Emits `AnimationUpdate` event via event bus with textures from `shape.get_textures()`
4. `SpriteRenderer` receives event and updates visual sprite (`app/engine/game_view/sprite_renderer.py`)

## Design Goals

1. **Separate state from visual data**: State (what entity is doing) should live in gameplay objects, not visual components
2. **Use event bus for rendering**: All animation updates should go through `app/core/event_bus/bus.py`
3. **Clarify UnitStates vs NpcAnimations**:
   - `UnitStates` = semantic states (IDLE, WALK, RUN, ATTACK) - what entity is *doing*
   - `NpcAnimations` = specific animation assets (ENEMY_IDLE, ARMED_WALK, etc.) - which spritesheet to use
4. **Support non-moving animated entities**: Future-proof for idle animations, interactive objects, etc.

## Proposed Architecture

### 1. State Management in CoordinateHolder

```python
class CoordinateHolder:
    - coordinates: CustomVec2i
    - visual_state: UnitStates  # NEW: IDLE, WALK, RUN, ATTACK, etc.
    - body: Body
    - shape: Shape
```

**Rationale**: CoordinateHolder is the right level because:
- Too high-level for Actor (doesn't know about movement/direction)
- Too restrictive for Unit (locks out non-Unit entities)
- CoordinateHolder knows position and can track activity state

### 2. Shape Becomes Pure Visual Configuration

```python
class Shape:
    - animations: AnimationCollection  # texture data organized by state+orientation
    - orientation: Directions  # NEW: FRONT, BACK, LEFT, RIGHT (for rendering)
    - animation_mapping: dict[UnitStates, NpcAnimations]  # NEW: state → animation data
```

**Key Changes**:
- Remove `current_animation` (moves to CoordinateHolder as `visual_state`)
- Rename `direction` to `orientation` (clarifies it's about facing, not movement)
- Add mapping between semantic states and animation assets

### 3. Direction vs Orientation vs Velocity

**Terminology clarification**:
- **Velocity** (in `BufferedMoverState`): Movement vector (x, y), used for physics/movement calculation
- **Orientation** (in `Shape`): Which way the sprite faces visually (FRONT/BACK/LEFT/RIGHT)
- **Direction** enum: Can be removed from movement logic, derived from velocity when needed

**Decision**: We don't need a separate direction in movement logic since velocity provides complete information. Orientation is purely visual and derived from velocity.

### 4. Animation Update Flow

#### Option A: Event-driven from Shape (Preferred by User)

```
BufferedMover calculates movement
    ↓
Updates CoordinateHolder.visual_state (e.g., IDLE → WALK)
    ↓
Updates Shape.orientation (based on velocity direction)
    ↓
Shape detects changes, emits AnimationUpdate event automatically
    ↓
Event payload contains: {coordinate_holder.name, textures}
    ↓
SpriteRenderer receives event and updates sprite
```

**Implementation approach**:
- Shape uses property setters to detect state/orientation changes
- When changed, Shape emits event automatically via event bus
- CoordinateHolder doesn't need to know about rendering

**User's comment**: "My previous crazy idea was in catching all the updates in Shape and emit event for CoordinateHolder and coordinateholder emits an event with name and animation data. It would be an overhead if we used kafka or something like this but within 1 process it could work."

#### Option B: Centralized AnimationController

```
BufferedMover calculates movement
    ↓
Updates CoordinateHolder.visual_state + Shape.orientation
    ↓
AnimationController behavior (runs each frame)
    ↓
Checks for visual_state or orientation changes
    ↓
Emits AnimationUpdate events for changed actors
    ↓
SpriteRenderer receives events
```

**User's comment**: "BufferedMover is not the best place to emit the event. Every animation update should be performed via some functionality (e.g. AnimationController you mentioned). The only thing, it is need to add the CoordinateHolder to payload as renderer should know what sprite is updated."

### 5. Future Considerations

**Non-moving animated entities**:
- "non-moving entities can I think. It is not currently needed but it would be convenient for interactive objects"
- No need for simultaneous animation states at the moment

**Orientation vs Direction**:
- "I think we can drop the direction for moving logic as velocity totally satisfies us here"
- "However, orientation is also important. For sightseeing. Could be brainstormed later."

## Open Questions for Next Session

### A. Animation Mapping Strategy

**Option 1**: Mapping defined per-instance in Shape
```python
shape = Shape(icon_path, animation_mapping={
    UnitStates.IDLE: NpcAnimations.ENEMY_IDLE,
    UnitStates.WALK: NpcAnimations.ENEMY_WALK,
    # ...
})
```

**Option 2**: Mapping defined per-entity-type (in a registry/factory)
```python
# In entity creation factory
goblin_animation_set = AnimationSet.GOBLIN  # pre-configured mapping
shape = Shape(icon_path, animation_set=goblin_animation_set)
```

### B. Shape Property Reactivity

For the "Shape emits events" approach, who manages the event emission?
- Should Shape have a reference to the CoordinateHolder (to get the name for events)?
- Or should CoordinateHolder subscribe to Shape changes and forward them?
- Or use Python properties with `__setattr__` magic to auto-emit?

### C. Orientation Update Responsibility

Who calculates the orientation from velocity?
- **BufferedMover** (knows velocity, updates orientation directly)
- **CoordinateHolder** (has a method `update_orientation_from_velocity()`)
- **Shape** (receives velocity, calculates internally)
- **AnimationController** (centralized logic)

### D. Non-moving Entities with Animations

For future-proofing idle animations on static objects:
- Should StaticObject also have `visual_state` and `Shape`?
- Or create a minimal `AnimatedObject` that only has shape but no body/coordinates?

## Key Files Referenced

- `app/core/geometry/shape.py:11` - Current Shape implementation
- `app/core/event_bus/bus.py` - Event bus for animation updates
- `app/core/event_bus/events.py` - AnimationUpdate event definition
- `app/core/event_bus/types.py` - AnimationUpdatePayload structure
- `app/objects/coordinate_holder.py:10` - CoordinateHolder class
- `app/objects/unit.py:9` - Unit class
- `app/objects/actor.py:16` - Actor base class
- `app/behaviours/moveable/buffered_mover.py:36` - Current animation update logic
- `app/engine/game_view/sprite_renderer.py` - Renderer that consumes animation events
- `app/config.py:17` - UnitStates enum definition
- `app/config.py:27` - NpcAnimations enum definition

## Next Steps

1. Decide on animation mapping strategy (per-instance vs registry)
2. Choose event emission approach (Shape reactivity vs AnimationController)
3. Determine orientation calculation responsibility
4. Design API for the new system
5. Plan migration path from current implementation