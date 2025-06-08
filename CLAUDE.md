# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a grid-based tactical game engine built with Pygame. The architecture follows an Entity-Component-System pattern combined with event-driven programming for turn-based tactical gameplay.

## Development Commands

### Running the Application
```bash
python main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

## Architecture

### Core System Flow
1. **Main Entry**: `main.py` initializes Pygame and starts the Application
2. **Game Loop**: `ui/application.py` runs at 60 FPS with fixed timestep
3. **Event Processing**: Input events are queued, processed, and dispatched to actors
4. **State Updates**: Actors process events and update their state
5. **Rendering**: Grid and sprites are drawn if state changes occurred

### Key Components

**Grid System** (`engine/grid.py`): 25x20 cell battlefield with unit placement and collision detection

**Actor System** (`ui/actors/`): Component-based entities with Actions, Controls, Body, and Behaviours
- Cursor actor for player interaction
- Pawn units with D&D-style stats (STR, DEX, CON, INT, WIS, CHA)
- Pluggable behavior system (Moveable, Aggressive, Frightened)

**Event System** (`event_processor/`): Sophisticated input handling with:
- Event subscription and buffering
- Timestamp tracking and event slicing
- Support for keyboard, gamepad, and scheduled events

**State Management** (`ui/state/`): 
- Actor registration and lifecycle
- Event bus with command pattern
- Conflict resolution between actors

**Rendering** (`ui/renderer.py`): Grid-based tile rendering with sprite scaling and visual feedback

### Configuration
- Game settings in `ui/config.py` (FPS, screen resolution, control mappings)
- Sprites located in `resources/icons/` (cursor.png, player.png, enemy.png)

## Code Patterns

- **ECS Architecture**: Actors are composed of modular components
- **Event-Driven**: Decoupled input handling through subscription model  
- **Command Pattern**: Actions are queued and batch processed
- **Strategy Pattern**: Swappable behaviors for different actor types

## Important Notes

- The `/app/` directory contains minimal/unused code - primary implementation is in `/ui/`
- Event processing uses timestamp-based slicing for precise timing
- Grid coordinates use (x, y) with origin at top-left
- All movements and actions go through conflict resolution before state commits