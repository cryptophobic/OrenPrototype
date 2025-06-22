# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a grid-based tactical game engine built with Pygame. The architecture follows an Entity-Component-System pattern combined with event-driven programming for turn-based tactical gameplay. **Note: This project is currently in early development with many systems partially implemented or commented out.**

## Development Commands

### Running the Application
```bash
python main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

Current dependencies: `pygame==2.6.0`, `petname==2.6`

## Architecture

### Core System Flow
1. **Main Entry**: `main.py` initializes the application and starts the game loop
2. **Game Loop**: `app/application.py` runs at 60 FPS with fixed timestep
3. **Context Management**: Level initialization and actor context setup
4. **Rendering**: Basic grid rendering (most game logic currently disabled)

### Key Components

**Application Core** (`app/application.py`): Main game loop with timestamp-based frame management
- Fixed 60 FPS rendering with interval-based updates
- Event system integration (currently commented out)
- State management integration (currently commented out)

**Actor System** (`app/objects/actor/`): Component-based entities with behavior patterns
- Base Actor class with behavior composition
- Support for multiple behaviors per actor (Moveable, Aggressive, Frightened, etc.)
- Action queuing and conflict resolution system
- Pending actions system with deferred execution

**Context System** (`app/context/`):
- Global context management for game state
- Actors context for entity management
- Frame context for timing and updates
- Grid context for spatial relationships

**Engine Components** (`app/engine/`):
- State management system (partially implemented)
- Event bus for message passing
- Grid system for spatial data
- Supervisor system (commented out)

**Input Processing** (`app/input_processor/`):
- Gamepad support
- Input event handling with timestamp tracking
- Scheduler for timed events
- Timer system for precise timing

**Configuration** (`app/config.py`):
- FPS: 60, Screen size: 1000x800
- Behavior enums (Moveable, Aggressive, Frightened, Watcher, etc.)
- Control mappings for different behaviors
- Color constants for rendering

**Resources** (`app/resources/icons/`):
- Sprite assets: cursor.png, player.png, enemy.png, walls.png

### Current State

**Working Systems:**
- Basic Pygame initialization and game loop
- Context management and level factory
- Actor system with behavior composition
- Basic renderer with grid display
- Input event processing framework

**Incomplete/Disabled Systems:**
- Most game logic is commented out in the main loop
- State manager updates are disabled
- Event dispatcher integration is commented out
- Supervisor system is not active
- Actor registration is incomplete

## Code Patterns

- **ECS-like Architecture**: Actors composed of pluggable behaviors
- **Context Pattern**: Global state management through context objects
- **Event-Driven**: Message bus and action queuing (partially implemented)
- **Command Pattern**: Action-based behavior execution
- **Factory Pattern**: Level creation through factory classes

## Interaction System Architecture

### Core Design Philosophy
The game implements a sophisticated **actor interaction system** based on command queuing, conflict resolution, and promise-based messaging. Key principles:

1. **Input → Action Translation**: Keyboard input maps to actor behavior actions
2. **Command Pipeline**: Queued action processing with conflict detection  
3. **Message-Based Conflict Resolution**: Actors communicate through message broker
4. **Promise System**: Asynchronous conflict resolution with rollback/retry
5. **Loop Prevention**: Guards against infinite actor interaction chains

### Interaction Flow
```
Input → ActorAction → CommandPipeline → BehaviorExecution
                                           ↓
Grid Update ← Success ←─────────────────── StateChange
                                           ↓
Conflict → MessageBroker → Promises → ReactionActions → Retry
```

### Key Components
- **ActorAction** (`app/bus/command_pipeline.py:9`): Encapsulates behavior method calls with retry logic
- **CommandPipeline** (`app/bus/command_pipeline.py:28`): Processes action queue with recursion protection
- **EventBus** (`app/engine/state/event_bus.py:30`): Message routing with sender/receiver ban system
- **Promise** (`app/bus/message_brocker.py:8`): Placeholder for async conflict resolution

### Conflict Resolution Process
1. Actor1 attempts action → Grid conflict detected
2. "Actor1 pushing you" message sent to conflicting actors
3. Actor1 state rolled back, action re-queued, becomes blocked
4. Target actors return Promises and queue reaction actions
5. After all reactions processed, Actor1's action retried
6. Ban system prevents infinite message loops (1 message/sender-receiver/frame)

See `INTERACTION_SYSTEM_DESIGN.md` for detailed architecture documentation.

## Development Status

This appears to be an early-stage refactoring of a tactical game engine. The **interaction system architecture** is well-designed but partially implemented. Core systems are in place but not fully integrated. The main game loop currently only handles basic rendering, with most gameplay logic disabled pending further development.