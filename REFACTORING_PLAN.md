# OrenPrototype Refactoring Plan

## Overview

This refactoring plan implements the behavior-driven architecture discussed in our conversation. The goal is to move from the current `/ui/`, `/engine/`, and `/map/` implementations to a clean, well-structured `/app/` directory with sophisticated behavior composition, event-driven state management, and flexible turn-based/real-time gameplay.

## Refactoring Goals

### Primary Objectives
1. **Implement Behavior-Driven Architecture**: Replace current control system with composable behaviors
2. **Create Sophisticated State Management**: Implement EventBus with conflict resolution and "pushed by" mechanics  
3. **Enable Dynamic Control Switching**: Support active/inactive actors with seamless turn-based to real-time transitions
4. **Build Height-Based Collision System**: Physical simulation using object weight, height, and unit stats

### Secondary Objectives
1. **Maintain Event Processor**: Keep existing `event_processor/` with minimal changes
2. **Improve Code Organization**: Clean separation of concerns in `/app/` structure
3. **Implement Unique Naming**: Petname-based actor ID system with collision resolution
4. **Add Level Loading System**: Python-based level initialization

## Current vs Target Architecture

### Current Structure (To Be Replaced)
```
/ui/                    # Primary implementation with Controls-based input
├── application.py      # Game loop with direct control binding
├── actors/            # Actor system with Controls dependency
├── state/             # Basic state management
└── renderer.py        # Rendering system

/engine/               # Duplicate/conflicting implementation
/map/                  # Basic map system
```

### Target Structure (New Implementation)
```
/app/                           # Clean refactored implementation
├── application.py              # Main game loop with supervisor integration
├── engine/                     # Core game systems
│   ├── grid.py                # Enhanced grid with height-based collision
│   ├── state.py               # Sophisticated state management
│   ├── supervisor.py          # Active state controller (NEW)
│   └── unit.py                # D&D-style units
├── object/                     # Object hierarchy (NEW)
│   ├── actor.py               # Base Actor class
│   ├── coordinate_holder.py   # Grid-placeable objects
│   ├── static_object.py       # Environmental objects
│   ├── unit.py                # RPG characters
│   └── behaviors/             # Behavior system (NEW)
│       ├── behaviour.py       # Base behavior interface
│       ├── moveable.py        # Movement behavior
│       ├── player.py          # Input handling behavior
│       ├── aggressive.py      # Combat behavior
│       ├── friend.py          # Faction behavior
│       ├── enemy.py           # Enemy behavior
│       └── frightened.py      # Defensive behavior
├── maps/                       # Level system (NEW)
│   └── levels/                # Python-based level files
│       ├── level1.py          # Level initialization
│       └── level2.py
└── helpers/                    # Utility modules
    └── vectors.py             # Vector mathematics

/event_processor/              # Keep with minimal changes
/resources/                    # Keep unchanged
```

## Implementation Phases

### Phase 1: Object Hierarchy Foundation
**Duration**: 2-3 days
**Priority**: Critical

#### 1.1 Create Base Actor Class (`app/object/actor.py`)
```python
class Actor:
    def __init__(self, name: str = None):
        self.name = name  # Will be set by ActorsCollection if None
        self.active = True
        self.dirty = False
        self.behaviors = {}
    
    def add_behavior(self, behavior_type: str, behavior):
        # Type validation goes here
        self.behaviors[behavior_type] = behavior
        self.dirty = True
    
    def remove_behavior(self, behavior_type: str):
        if behavior_type in self.behaviors:
            del self.behaviors[behavior_type]
            self.dirty = True
    
    def get_action(self, key: int) -> Callable:
        # Return action from Player behavior if present
        pass
    
    def produce_event(self, event_type: str, data: dict):
        # Event production capability
        pass
```

#### 1.2 Create CoordinateHolder (`app/object/coordinate_holder.py`)
```python
from app.object.actor import Actor
from app.helpers.vectors import Vec2

class CoordinateHolder(Actor):
    def __init__(self, coordinates: Vec2, name: str = None):
        super().__init__(name)
        self.coordinates = coordinates
        self.position = coordinates  # Current grid position
        self.collision_response = "OVERLAP"  # Configurable
    
    def is_conflicting(self, other: 'CoordinateHolder') -> bool:
        # Collision detection logic
        pass
    
    def clear_velocity(self):
        # Reset movement for conflict resolution
        pass
```

#### 1.3 Create StaticObject and Unit Classes
- **StaticObject**: Environmental objects with weight, height, physical properties
- **Unit**: RPG characters with D&D stats (STR, DEX, CON, INT, WIS, CHA)

### Phase 2: Behavior System Implementation
**Duration**: 3-4 days
**Priority**: Critical

#### 2.1 Base Behavior Interface (`app/object/behaviors/behaviour.py`)
```python
from abc import ABC, abstractmethod
from typing import Callable, Dict

class Behaviour(ABC):
    def __init__(self, actor):
        self.actor = actor
    
    @abstractmethod
    def get_actions(self) -> Dict[int, Callable]:
        """Return mapping of pygame keys to action callables"""
        pass
    
    @abstractmethod
    def is_compatible_with(self, actor_type: type) -> bool:
        """Check if behavior can be applied to actor type"""
        pass
```

#### 2.2 Core Behavior Implementations

**Moveable Behavior** (`app/object/behaviors/moveable.py`)
- Available to: CoordinateHolder and inheritors
- Actions: move_up, move_down, move_left, move_right
- Pygame key mappings for movement

**Player Behavior** (`app/object/behaviors/player.py`)
- Connects to keyboard/gamepad input
- Only behavior that interfaces with EventsHandler
- Multiple player support with different control schemes

**Combat Behaviors** (`aggressive.py`, `friend.py`, `enemy.py`, `frightened.py`)
- Available to: Unit class only
- Define combat capabilities and faction allegiances
- Actions: attack, defend, dodge, end_turn

#### 2.3 Behavior Composition System
- Type validation at compile time
- Dynamic add/remove with dirty flag management
- Behavior dependency checking (optional)

### Phase 3: State Management System
**Duration**: 4-5 days
**Priority**: Critical

#### 3.1 ActorsCollection (`app/engine/actors_collection.py`)
```python
from collections import UserDict
import petname
import random
import time

class ActorsCollection(UserDict[str, Actor]):
    def add_actor(self, actor: Actor) -> str:
        if actor.name and actor.name not in self.data:
            name = actor.name
        else:
            name = self.generate_unique_name()
            actor.name = name
        
        self.data[name] = actor
        return name
    
    def generate_unique_name(self) -> str:
        base_name = petname.Generate(2, separator="-")
        timestamp = int(time.time() * 1000) % 10000
        name = f"{base_name}-{timestamp}"
        
        if name in self.data:
            counter = timestamp + 1
            while f"{base_name}-{counter}" in self.data:
                counter += 1
            name = f"{base_name}-{counter}"
        
        return name
    
    def get_active_actors(self) -> List[Actor]:
        return [actor for actor in self.data.values() if actor.active]
    
    def get_dirty_actors(self) -> List[Actor]:
        return [actor for actor in self.data.values() if actor.dirty]
```

#### 3.2 EventsHandler (`app/engine/events_handler.py`)
```python
class EventsHandler:
    def __init__(self, actors_collection: ActorsCollection):
        self.actors = actors_collection
        self.__keys: Dict[int, set[str]] = {}  # pygame key -> actor names
    
    def load_keys_from_actor(self, actor: Actor):
        if "player" in actor.behaviors:
            player_behavior = actor.behaviors["player"]
            for key, action in player_behavior.get_actions().items():
                if key not in self.__keys:
                    self.__keys[key] = set()
                self.__keys[key].add(actor.name)
    
    def unload_keys_from_actor(self, actor: Actor):
        for key_set in self.__keys.values():
            key_set.discard(actor.name)
    
    def dispatch_events(self, events: deque[EventLogRecord]):
        # Process events for Player-controlled actors only
        pass
```

#### 3.3 EventBus with Conflict Resolution (`app/engine/event_bus.py`)
```python
class EventBus:
    def __init__(self, grid):
        self.grid = grid
        self.action_queue = deque()
    
    def post(self, actor: Actor, action: Callable):
        self.action_queue.append((actor, action))
    
    def process_actions(self) -> bool:
        # Process all queued actions
        # Handle conflict resolution with "pushed by" mechanics
        # Return True if any state changes occurred
        pass
    
    def handle_movement_conflict(self, actor, target_cell):
        # Generate "pushed by" actions for displaced objects
        # Implement height-based collision for static objects
        pass
```

#### 3.4 Unified State Manager (`app/engine/state.py`)
```python
class State:
    def __init__(self, grid):
        self.grid = grid
        self.actors = ActorsCollection()
        self.events_handler = EventsHandler(self.actors)
        self.event_bus = EventBus(self.grid)
    
    def register_actor(self, actor: Actor):
        name = self.actors.add_actor(actor)
        self.events_handler.load_keys_from_actor(actor)
        return name
    
    def queue_action(self, actor: Actor, action: Callable):
        """Safe API for AI action injection"""
        self.event_bus.post(actor, action)
    
    def update_state(self, events: deque[EventLogRecord]):
        # Process dirty actors first
        for actor in self.actors.get_dirty_actors():
            self.events_handler.unload_keys_from_actor(actor)
            self.events_handler.load_keys_from_actor(actor)
            actor.dirty = False
        
        # Dispatch input events
        self.events_handler.dispatch_events(events)
    
    def commit(self) -> bool:
        return self.event_bus.process_actions()
```

### Phase 4: Supervisor Agent System
**Duration**: 2-3 days
**Priority**: High

#### 4.1 Supervisor Agent (`app/engine/supervisor.py`)
```python
class SupervisorAgent:
    def __init__(self, state_manager: State):
        self.state = state_manager
        self.mode = "turn_based"  # or "real_time"
        self.current_player = None
    
    def set_mode(self, mode: str):
        self.mode = mode
    
    def activate_actor(self, actor_name: str):
        if actor_name in self.state.actors:
            self.state.actors[actor_name].active = True
    
    def deactivate_actor(self, actor_name: str):
        if actor_name in self.state.actors:
            self.state.actors[actor_name].active = False
    
    def switch_active_player(self, new_player: str):
        if self.current_player:
            self.deactivate_actor(self.current_player)
        self.activate_actor(new_player)
        self.current_player = new_player
    
    def update(self):
        # Run before state_manager.update_state()
        # Implement turn-based logic or real-time AI activation
        pass
```

#### 4.2 Game Mode Management
- Turn-based mode: Single active player at a time
- Real-time mode: Multiple active actors simultaneously
- Dynamic switching between modes
- AI activation scheduling

### Phase 5: Enhanced Grid and Collision System
**Duration**: 3-4 days
**Priority**: Medium

#### 5.1 Enhanced Grid (`app/engine/grid.py`)
```python
class Cell:
    def __init__(self, coordinates: Vec2, height=0):
        self.coordinates = coordinates
        self.height = height
        self.occupants = []  # Multiple objects can occupy same cell
        self.selected = False
    
    def add_occupant(self, obj):
        self.occupants.append(obj)
    
    def remove_occupant(self, obj):
        if obj in self.occupants:
            self.occupants.remove(obj)
    
    def can_accommodate(self, new_obj) -> bool:
        # Check height-based collision with unit stats
        pass

class Grid:
    def __init__(self, width=25, height=20):
        self.width = width
        self.height = height
        self.cells = [[Cell(Vec2(x=x, y=y)) for x in range(width)] for y in range(height)]
    
    def move_object(self, obj, from_pos: Vec2, to_pos: Vec2) -> bool:
        # Enhanced movement with conflict resolution
        pass
    
    def get_collision_response(self, obj1, obj2) -> str:
        # Collision matrix lookup
        pass
```

#### 5.2 Collision Matrix System
- Define interaction rules between object types
- Height-based calculations using unit stats
- "Pushed by" action generation for displaced objects

### Phase 6: Level Loading System
**Duration**: 2-3 days
**Priority**: Medium

#### 6.1 Level Structure (`app/maps/levels/level1.py`)
```python
from app.engine.grid import Grid
from app.object.unit import Unit
from app.object.static_object import StaticObject
from app.helpers.vectors import Vec2

def initialize_level() -> Grid:
    grid = Grid(25, 20)
    
    # Place static objects
    tree = StaticObject(Vec2(5, 5), "tree")
    tree.add_behavior("solid", SolidBehavior())
    grid.place_object(tree, Vec2(5, 5))
    
    # Place units
    player = Unit(Vec2(1, 1), "player-hero")
    player.add_behavior("moveable", MoveableBehavior(player))
    player.add_behavior("player", PlayerBehavior(player))
    grid.place_object(player, Vec2(1, 1))
    
    return grid
```

#### 6.2 Dynamic Level Loading
- Python-based level definitions
- Object placement with behavior assignment
- Grid initialization with proper dimensions

### Phase 7: Application Integration
**Duration**: 2-3 days
**Priority**: High

#### 7.1 Enhanced Application Loop (`app/application.py`)
```python
class Application:
    def __init__(self, level_loader):
        self.grid = level_loader()
        self.state_manager = State(self.grid)
        self.supervisor = SupervisorAgent(self.state_manager)
        self.event_dispatcher = InputEvents()
        # ... existing setup
    
    def run(self):
        while not self.game_over:
            self.ticker.tick()
            self.check_exit()
            self.event_dispatcher.listen(self.ticker.last_timestamp)
            
            if self.ticker.last_timestamp >= render_threshold:
                # NEW: Supervisor runs first
                self.supervisor.update()
                
                events = self.event_dispatcher.slice_flat(first_timestamp, render_threshold)
                self.state_manager.update_state(events)
                
                if self.state_manager.commit():
                    self.renderer.draw()
```

## Implementation Strategy

### Week 1: Foundation
- [ ] Create `/app/` directory structure
- [ ] Implement Actor hierarchy (Actor → CoordinateHolder → StaticObject/Unit)
- [ ] Basic behavior interface and Moveable behavior
- [ ] Unit tests for object hierarchy

### Week 2: Behavior System
- [ ] Complete all core behaviors (Player, Aggressive, Friend, Enemy, Frightened)
- [ ] Behavior composition system with type validation
- [ ] Dynamic behavior add/remove with dirty flag system
- [ ] Integration tests for behavior composition

### Week 3: State Management
- [ ] ActorsCollection with unique naming system
- [ ] EventsHandler for Player behavior input processing
- [ ] EventBus with basic action queuing
- [ ] Unified State manager integration

### Week 4: Advanced Features
- [ ] Conflict resolution and "pushed by" mechanics
- [ ] Height-based collision system
- [ ] Supervisor agent implementation
- [ ] Turn-based/real-time mode switching

### Week 5: Integration and Testing
- [ ] Enhanced Grid system with multi-occupancy
- [ ] Level loading system implementation
- [ ] Application loop integration
- [ ] Comprehensive testing and bug fixes

## Risk Mitigation

### High Risk Areas
1. **Behavior Type Validation**: Complex compile-time checking
   - **Mitigation**: Start with simple runtime validation, enhance later
2. **Event System Integration**: Maintaining compatibility with existing event_processor
   - **Mitigation**: Minimal changes to event_processor, adapter pattern if needed
3. **Performance Impact**: New systems may affect 60 FPS target
   - **Mitigation**: Profile early, optimize critical paths

### Medium Risk Areas
1. **Collision System Complexity**: Height-based calculations may be complex
   - **Mitigation**: Implement basic version first, enhance iteratively
2. **State Synchronization**: Multiple state components need coordination
   - **Mitigation**: Clear interface contracts, comprehensive testing

## Testing Strategy

### Unit Tests
- Object hierarchy methods and properties
- Behavior composition and validation
- ActorsCollection unique naming
- Grid collision detection

### Integration Tests
- Behavior system with state management
- Event flow from input to grid updates
- Supervisor agent mode switching
- Level loading and object placement

### Performance Tests
- 60 FPS maintenance with multiple active actors
- Memory usage with behavior composition
- Event processing throughput

## Success Criteria

1. **Functional Criteria**
   - All current gameplay features maintained
   - Behavior composition working correctly
   - Dynamic control switching functional
   - Conflict resolution with "pushed by" mechanics

2. **Code Quality Criteria**
   - Clean separation of concerns in `/app/` structure
   - Type safety with behavior validation
   - Comprehensive test coverage (>80%)
   - Documented APIs and architectural decisions

3. **Performance Criteria**
   - Maintain 60 FPS target
   - Memory usage remains reasonable
   - Startup time not significantly increased

## Post-Refactoring Steps

1. **Code Cleanup**: Remove old `/ui/`, `/engine/`, `/map/` directories
2. **Documentation Update**: Update CLAUDE.md with new architecture
3. **Performance Optimization**: Profile and optimize critical paths
4. **Feature Enhancement**: Add new behaviors and game mechanics
5. **UE Migration Preparation**: Document behavior system for GAS integration

This refactoring plan transforms the current prototype into a sophisticated, behavior-driven RPG engine that supports complex gameplay scenarios while maintaining clean, extensible code architecture.