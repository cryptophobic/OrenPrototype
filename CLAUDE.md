# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a grid-based tactical game engine built with Pygame. The architecture follows an Entity-Component-System pattern combined with event-driven programming for turn-based tactical gameplay. The project features sophisticated systems for actor interaction, message passing, and behavior composition.

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
3. **Input Processing**: Event collection and keyboard input handling
4. **Command Pipeline**: Action queuing and execution with conflict resolution
5. **Rendering**: Grid-based visual output

### Key Components

**Application Core** (`app/application.py:11`): Main game loop with timestamp-based frame management
- Fixed 60 FPS rendering with interval-based updates
- Input event processing and slicing by timeframe
- Integrated systems (state management and supervisor currently disabled)

**Actor System** (`app/objects/actor.py:12`): Component-based entities with behavior composition
- Base Actor class with pluggable behaviors 
- Message handling and response generation
- Pending action queues for deferred execution
- Behavior checking and management methods

**Behavior System** (`app/behaviours/behaviour.py:21`): Modular behavior components
- Message handler registration with decorators
- Type-safe message routing to receiver methods
- Grid and message broker integration
- Support for different receiver types

**Command Pipeline** (`app/engine/command_pipeline/pipeline.py:39`): Action processing engine
- ActorAction wrapper with retry logic and resolution tracking
- Recursive action processing with depth protection (max 5 levels)
- Pending action flushing and re-queuing
- State change tracking and queue management

**Message Broker** (`app/engine/message_broker/broker.py:10`): Inter-actor communication
- Promise-based message delivery system
- Response queuing and retrieval
- Actor activity checking before message delivery

**Input Processing** (`app/engine/input_processor/InputEvents.py:29`): Sophisticated input handling
- Key subscription system with repeat intervals
- Event logging with timestamps
- Time-sliced event retrieval (flat and grouped)
- Gamepad and scheduler integration
- Automatic event log flushing

**Journal System** (`app/journal/journal.py:27`): Development-focused logging
- Property and method access tracking
- Timestamp-based event recording
- Context-aware logging with frame integration
- Attribute read/write/call monitoring

**Collections** (`app/collections/actors_collection.py:11`): Type-safe entity management
- Generic actor collections with filtering
- Active/pending/deleted state management
- Type-based actor retrieval
- Unique name generation and conflict resolution

**Configuration** (`app/config.py:1`):
- FPS: 60, Screen size: 1000x800
- Behavior enums covering actors, units, coordinate holders, and static objects
- Color constants for rendering

### Current Implementation Status

**Fully Implemented Systems:**
- Actor behavior composition and message handling
- Command pipeline with retry logic and recursion protection
- Input event processing with time-slicing capabilities
- Message broker with promise-based responses
- Journal system for development debugging
- Type-safe collections with generic constraints
- Basic rendering and game loop structure

**In Progress/Partially Implemented:**
- Grid system integration (referenced but not fully connected)
- State management (infrastructure present, disabled in main loop)
- Supervisor system (commented out in application)
- Actor registration (infrastructure ready, not active)

**Architecture Strengths:**
- Protocol-based design with clear interfaces
- Type safety with generics and TypeVars
- Separation of concerns between systems
- Event-driven architecture with message passing
- Sophisticated conflict resolution capabilities

## Code Patterns

- **Protocol-Based Architecture**: Clear interfaces defined in `app/protocols/`
- **Generic Collections**: Type-safe containers with filtering capabilities  
- **Message-Driven Communication**: Actors communicate via message broker
- **Command Pattern**: Actions encapsulated as objects with retry logic
- **Decorator Pattern**: Message handler registration via decorators
- **Factory Pattern**: Level creation and unique name generation

## Development Focus Areas

The codebase shows active development in:
1. **Journal System**: New logging infrastructure for development debugging
2. **Input Processing**: Sophisticated keyboard input handling with time-slicing
3. **Command Pipeline**: Robust action processing with conflict resolution
4. **Message System**: Promise-based inter-actor communication

The architecture is well-designed for complex tactical gameplay with turn-based mechanics, sophisticated AI behaviors, and real-time input processing.