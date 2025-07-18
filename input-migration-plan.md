# Input System Migration Plan: From Discrete Events to Continuous State

## Current System Analysis

### Existing Architecture (`app/engine/input_processor/InputEvents.py`)
- **Event-driven**: Logs discrete key down/up events with timestamps
- **Tick-based**: Uses ticks/timestamps for timing, designed for fixed timestep simulation
- **Auto-repeat**: Sophisticated repeat logic with configurable intervals
- **Time-slicing**: Can retrieve events within specific time ranges
- **Subscription model**: Actors subscribe to specific keys with repeat intervals
- **Perfect for**: Turn-based gameplay, discrete actions, input replay

### Key Components
1. **InputEvents**: Main event logger with subscription management
2. **Scheduler**: Time-based key event scheduling
3. **InputHandler**: Message broker integration for actor communication
4. **Gamepads**: Controller input support

## Target: Arcade-Friendly Continuous System

### Arcade Input Patterns
- **Velocity-based**: Set velocities in `on_key_press`/`on_key_release`
- **Delta time**: Use `delta_time` in `on_update()` for frame-rate independence
- **State-based**: Continuous key state checking rather than discrete events
- **Animation-friendly**: Smooth interpolation for sliding/tween animations

## Migration Strategy

### Phase 1: Dual System Implementation
**Goal**: Keep existing system while introducing continuous state tracking

#### 1.1 Create Continuous Input State Manager
```python
# app/engine/input_processor/ContinuousInput.py
class ContinuousInputState:
    def __init__(self):
        self.key_states: Dict[int, bool] = {}
        self.key_velocities: Dict[int, float] = {}
        self.subscribers: Dict[str, Set[int]] = {}
    
    def set_key_state(self, key: int, pressed: bool):
        self.key_states[key] = pressed
    
    def is_key_pressed(self, key: int) -> bool:
        return self.key_states.get(key, False)
    
    def get_movement_vector(self, keys: Dict[int, Tuple[float, float]]) -> Tuple[float, float]:
        # Calculate combined movement vector from pressed keys
        pass
```

#### 1.2 Integrate with Existing Message System
- Extend existing `MessageTypes` with continuous input messages
- Add `ContinuousInputPayload` for velocity/state updates
- Modify `InputHandler` to support both discrete and continuous modes

#### 1.3 Add Delta Time Support
- Extend current Timer system to provide delta time
- Create delta-time aware movement helpers
- Add interpolation utilities for smooth animations

### Phase 2: Animation and Movement System
**Goal**: Enable smooth actor movement and animations

#### 2.1 Create Movement Component System
```python
# app/behaviours/actor/movement.py
class MovementBehaviour:
    def __init__(self):
        self.velocity: Vector2 = Vector2(0, 0)
        self.target_position: Optional[Vector2] = None
        self.movement_speed: float = 5.0
        self.is_moving: bool = False
    
    def set_velocity_from_input(self, input_vector: Tuple[float, float]):
        pass
    
    def slide_to_position(self, target: Vector2, duration: float):
        pass
    
    def update(self, delta_time: float):
        # Update position based on velocity and delta time
        pass
```

#### 2.2 Animation Integration
- Create tween/interpolation system for smooth tile-to-tile movement
- Add easing functions (ease-in, ease-out, linear)
- Support for queued movements and animation chaining

### Phase 3: Hybrid Input Processing
**Goal**: Support both discrete events and continuous state simultaneously

#### 3.1 Input Mode Selection
```python
class InputMode(Enum):
    DISCRETE = "discrete"    # Original tick-based events
    CONTINUOUS = "continuous"  # Delta-time based state
    HYBRID = "hybrid"        # Both systems active
```

#### 3.2 Behavior-Level Input Configuration
- Allow behaviors to specify preferred input mode
- Route input through appropriate system based on behavior needs
- Support mode switching during gameplay

### Phase 4: Migration Tools and Compatibility
**Goal**: Provide tools to ease migration of existing code

#### 4.1 Input Adapter Layer
```python
# app/engine/input_processor/InputAdapter.py
class InputAdapter:
    """Provides backward compatibility for discrete event consumers"""
    
    def convert_continuous_to_discrete(self, continuous_state: ContinuousInputState, 
                                     delta_time: float) -> KeyPressEventLogRecords:
        # Convert current continuous state to discrete events
        pass
    
    def emulate_key_repeat(self, key: int, repeat_interval: float) -> bool:
        # Emulate auto-repeat behavior using continuous state
        pass
```

#### 4.2 Migration Utilities
- Code analyzer to identify discrete input dependencies
- Automatic behavior annotation for input mode preferences
- Performance profiler for input system overhead

## Implementation Timeline

### Week 1-2: Foundation
- [ ] Implement `ContinuousInputState` class
- [ ] Extend message types for continuous input
- [ ] Add delta time support to existing Timer system
- [ ] Create basic movement behavior template

### Week 3-4: Core Features
- [ ] Implement movement interpolation system
- [ ] Add animation/tween support
- [ ] Create input adapter for backward compatibility
- [ ] Extend InputHandler for dual-mode support

### Week 5-6: Integration
- [ ] Integrate continuous input with existing actors
- [ ] Add behavior-level input mode configuration
- [ ] Implement smooth tile-to-tile movement
- [ ] Create migration utilities and documentation

### Week 7-8: Optimization & Testing
- [ ] Performance testing and optimization
- [ ] Complete backward compatibility testing
- [ ] Documentation and examples
- [ ] Migration guide for existing behaviors

## Benefits After Migration

### For Animation & Movement
- **Smooth interpolation**: Actors can slide smoothly between tiles
- **Frame-rate independence**: Consistent movement regardless of FPS
- **Delta-time animations**: Precise timing for tween sequences
- **Velocity-based physics**: Natural acceleration/deceleration

### For Game Development
- **Modern arcade patterns**: Follows standard arcade input handling
- **Hybrid capability**: Support both real-time and turn-based mechanics
- **Better responsiveness**: Immediate input response for continuous actions
- **Animation-friendly**: Built-in support for complex movement sequences

### Maintained Capabilities
- **Turn-based support**: Discrete events still available via adapter
- **Input replay**: Can reconstruct discrete events from continuous state
- **Time-slicing**: Adapter can provide time-sliced input for simulation
- **Subscription model**: Enhanced with input mode preferences

## Risk Mitigation

1. **Backward Compatibility**: Input adapter ensures existing code continues working
2. **Performance**: Continuous state tracking has minimal overhead compared to event logging
3. **Complexity**: Phased implementation allows gradual adoption
4. **Testing**: Dual system allows A/B testing of input approaches

## Success Metrics

- [ ] All existing discrete input functionality preserved
- [ ] Smooth 60fps actor movement achieved
- [ ] Animation system supports complex movement sequences
- [ ] Zero breaking changes to existing behavior code
- [ ] Performance equal or better than current system