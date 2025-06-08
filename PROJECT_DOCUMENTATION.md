# OrenPrototype - Turn-Based RPG Engine Documentation

## Project Overview

OrenPrototype is a sophisticated turn-based RPG game engine prototype built with Pygame. The engine implements a flexible behavior-driven architecture that supports both turn-based and real-time gameplay modes, with dynamic actor control switching and advanced collision resolution. This prototype serves as a foundation for future Unreal Engine implementation with Gameplay Ability System (GAS).

## Architecture Overview

### Core Design Patterns

1. **Behavior-Driven Architecture**: Strategy pattern with composable behaviors that define object capabilities and actions
2. **Event-Driven State Management**: Sophisticated event bus system with conflict resolution and "pushed by" mechanics
3. **Dynamic Control Switching**: Active/inactive actor states enabling seamless turn-based to real-time transitions
4. **Height-Based Collision System**: Physics simulation using object weight, height, and unit stats for realistic interactions

### System Flow

```
Main Entry (main.py)
    ↓
Application Loop (app/application.py) - 60 FPS
    ↓
Supervisor Agent - Manages active/inactive states (turn-based/real-time modes)
    ↓
Input Processing - Player behaviors listen to keyboard/gamepad events
    ↓
Action Generation - Both player inputs and AI logic generate actions
    ↓
Event Bus - Queues and processes actions with conflict resolution
    ↓
Grid Updates - Height-based collision with "pushed by" mechanics
    ↓
State Commit - Only render if state changes occurred
```

## Object Hierarchy

### Actor (Base Class)
- **Purpose**: Base class for all game objects that can produce events
- **Grid Placement**: Cannot be placed on grid
- **Use Cases**: Save, load, quit operations
- **Key Features**: Event production, unique naming system

### CoordinateHolder(Actor)
- **Purpose**: Objects that can be placed on the grid
- **Grid Placement**: Can be placed on grid without body
- **Collision Response**: Usually OVERLAP (configurable)
- **Use Cases**: Cursor for hovering and selecting
- **Key Features**: Position management, basic collision detection

### StaticObject(CoordinateHolder)
- **Purpose**: Environmental objects with physical properties
- **Properties**: Solid, soft, weight, height (set via behavior strategy pattern)
- **Use Cases**: Trees, rocks, walls, chests
- **Collision**: Height-based interaction with units
- **Key Features**: Environmental interaction, strategic positioning

### Unit(CoordinateHolder)
- **Purpose**: Characters with RPG stats and combat capabilities
- **Stats**: STR, DEX, CON, INT, WIS, CHA (D&D-style)
- **Types**: Player characters, enemies, NPCs, various species
- **Key Features**: Combat stats, behavior composition, faction management

## Behavior System

### Core Behaviors

**Moveable**
- Allows object to move on the grid
- Available to: CoordinateHolder and all inheritors
- Actions: Movement in cardinal directions

**Aggressive**
- Enables combat and defense capabilities
- Available to: Units only
- Actions: Attack, defend, combat maneuvers

**Player**
- Connects actor to keyboard/gamepad input
- Handles input-to-action mapping
- Only Player-controlled entities listen to input events

**Friend/Enemy**
- Determines faction and combat targeting
- Friend: Fights on current player's side
- Enemy: Fights against current player
- Available to: Units only

**Frightened**
- Defensive behavior patterns
- Modifies movement and combat decisions
- Available to: Units only

### Behavior Composition Rules

- **Multiple Behaviors**: Objects can have multiple behaviors simultaneously
- **Type Restrictions**: Not all behaviors suit all classes (e.g., CoordinateHolder can be Moveable but not Friend/Enemy)
- **Dynamic Management**: Behaviors can be added/removed at runtime
- **Input Binding**: Only Player behavior connects to input system

## State Management System

### Core Components

**State Manager (`app/engine/state.py`)**
- Manages four core states: Grid, ActorsCollection, EventsHandler, EventBus
- Handles dirty object reregistration
- Provides safe API for AI action injection
- Implements commit pattern for atomic updates

**ActorsCollection (UserDict[str, Actor])**
- Manages all game actors with unique IDs
- ID Format: `{petname}-{number}` (e.g., "happy-cat-742")
- Features: Filter by active/dirty states, lifecycle management
- Unique naming with fallback generation

**EventsHandler**
- Connects keyboard inputs to Player-controlled actors
- Key mapping: `Dict[int: set[str]]` (pygame key codes to actor names)
- Only processes Player behavior actors
- Methods: `load_keys_from_actor()`, `unload_keys_from_actor()`, `dispatch_events()`

**EventBus**
- Queues and processes all actions (player and AI)
- Handles conflict resolution through collision matrix
- Implements "pushed by" mechanics for displaced objects
- First-come-first-served action prioritization

### Active State Management

**Supervisor Agent (`app/engine/supervisor.py`)**
- Controls which actors are active/inactive
- Supports two modes: Turn-based and Real-time
- Runs before `state_manager.update_state(events)`
- Manages player switching and AI activation

**Active Property System**
- Each Actor has `active` boolean property
- Inactive actors ignore all events
- Enables dynamic control switching between players
- Supports party-based control with shared input

## Grid and Collision System

### Grid Structure (`app/engine/grid.py`)
- 25x20 cell battlefield
- Each cell tracks: coordinates, height, unit occupancy, selection state
- Shared reference between EventBus and State Manager

### Collision Resolution

**Basic Collision**
- CoordinateHolder objects can have configurable collision responses
- Default responses: OVERLAP, BLOCK, etc.

**Height-Based Collision (Static Objects)**
- Units can share cells with static objects if height is manageable
- Height calculation uses unit stats (STR, DEX, etc.)
- Both objects remain in cell and receive events normally

**Conflict Resolution**
- When movement conflicts occur, "pushed by" actions are generated
- Displaced objects get chance to react based on weight and properties
- Second attempt uses collision matrix only
- Prevents infinite push chains

## Event Processing

### Input Flow
```
Keyboard/Gamepad Input
    ↓
EventsHandler (Player behaviors only)
    ↓
Action Generation via Behaviors
    ↓
State Manager queue_action()
    ↓
EventBus processing
    ↓
Grid collision resolution
    ↓
State updates
```

### AI Action Injection
```
AI Logic
    ↓
Direct action generation
    ↓
State Manager queue_action()
    ↓
EventBus processing (bypasses input system)
```

### Event Processing Features
- 60 FPS processing with first-come-first-served priority
- Non-blocking system allows simultaneous actions (like Baldur's Gate 3)
- Dirty flag system for behavior changes triggers reregistration
- Commit-based rendering only updates on state changes

## Level System

### Level Loading (`app/maps/levels/`)
- Python code that initializes grid state
- Creates and places all initial objects
- Defines starting positions, static objects, units
- Example files: `level1.py`, `level2.py`, etc.

### Level Structure
- Grid initialization with specified dimensions
- Static object placement (trees, rocks, walls, chests)
- Unit spawning with stats and initial behaviors
- Environmental setup and configuration

## Performance Considerations

### Optimization Features
- **Conditional Rendering**: Only render when `commit()` returns True
- **Dirty Flag System**: Efficient behavior reregistration
- **Event Batching**: Process multiple events per frame
- **Shared Grid Reference**: Avoid data duplication

### Scalability Notes
- Designed as prototype for Unreal Engine migration
- 60 FPS target maintained with current architecture
- Event system designed to handle multiple simultaneous actors
- Modular design allows easy component swapping

## Development Workflow

### Dependencies
```bash
pip install -r requirements.txt
```

### Running the Game
```bash
python main.py
```

### Project Structure
```
/app/                           # Refactored clean implementation
├── application.py              # Main game loop
├── engine/                     # Core game systems
│   ├── grid.py                # Grid and collision system
│   ├── state.py               # State management
│   ├── supervisor.py          # Active state controller
│   └── unit.py                # Unit definitions
├── object/                     # Object hierarchy
│   ├── actor.py               # Base Actor class
│   ├── coordinate_holder.py   # Grid-placeable objects
│   ├── static_object.py       # Environmental objects
│   ├── unit.py                # RPG characters
│   └── behaviors/             # Behavior implementations
│       ├── behaviour.py       # Base behavior interface
│       ├── moveable.py        # Movement behavior
│       ├── aggressive.py      # Combat behavior
│       └── ...                # Additional behaviors
├── maps/                       # Level definitions
│   └── levels/                # Individual level files
│       ├── level1.py          # Level initialization code
│       └── level2.py
└── helpers/                    # Utility modules
    └── vectors.py             # Vector mathematics

/ui/                           # Current implementation (to be replaced)
/engine/                       # Current implementation (to be replaced)
/event_processor/              # Event system (minimal changes needed)
/map/                          # Current map system (to be replaced)
```

## Key Implementation Notes

### Behavior System Design
- Behaviors provide actions as Callable objects
- State manager maintains behavior-action connections
- Dynamic behavior registration/unregistration
- Type safety through compile-time behavior validation

### Naming and ID System
- Unique actor IDs with meaningful names when possible
- Petname generation with timestamp/counter fallbacks
- Collision-free naming system

### Event System Philosophy
- Non-blocking real-time processing
- Conflict resolution through gameplay mechanics
- Emergent gameplay through "pushed by" interactions
- Support for both human and AI players

## Future Enhancements

### Immediate Goals
- Complete refactoring from `/ui/` to `/app/` structure
- Implement supervisor agent for turn management
- Finalize behavior system with proper type constraints
- Add comprehensive collision matrix

### Long-term Vision
- Migration to Unreal Engine with GAS
- Enhanced AI behavior trees
- Multiplayer networking support
- Advanced visual effects and animation
- Save/load functionality with behavior serialization

This architecture provides a solid foundation for a flexible, extensible turn-based RPG engine with the capability to support complex gameplay scenarios and smooth transition to more advanced game engines.