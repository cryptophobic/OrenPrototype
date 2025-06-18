# Interaction System Design

## Overview

This document formalizes the actor interaction system for the tactical game engine, outlining how actors communicate, resolve conflicts, and maintain state consistency through a command pipeline and message broker architecture.

## Core Interaction Flow

### 1. Input to Action Translation
- **Keyboard input** is mapped to specific **actor behavior actions**
- Each behavior (Moveable, Aggressive, Frightened) has associated control mappings
- Input events are translated into `ActorAction` objects containing:
  - Target actor
  - Behavior type
  - Method name
  - Arguments and parameters

### 2. State Manager Processing  
- **State Manager** reads input and extracts registered actions
- Actions are queued in the **Command Pipeline** (not EventBus)
- Each action represents an **attempt to change actor state**

### 3. Action Execution
- **Executing an action** = changing actor state + updating Grid position
- Actions are processed through behavior methods on the target actor
- Success/failure is determined by grid constraints and actor state

### 4. Conflict Detection and Messaging
- If action **fails due to conflicts** with other actors:
  - Generate a "block response" 
  - Actor1 sends message: "Actor1 pushing you" to conflicted actors
  - Actor1's state is **rolled back**
  - Original action is **re-queued** in Command Pipeline
  - Actor1 becomes **blocked** until conflicts resolve (or frame ends)

### 5. Promise-Based Conflict Resolution
- **Every actor receives messages immediately**
- Non-blocked actors return a **Promise** to Actor1
- Promise represents commitment to react to the message
- Blocked actors cannot make promises until unblocked

### 6. Reactive Action Generation
- **Reacting to messages** = putting new actions into Command Pipeline
- Reactions are derived from actor behaviors
- New actions enter the same processing cycle

### 7. Retry Mechanism
- When **all conflict actions are processed**, Command Pipeline retries Actor1's original action
- This creates a cascading resolution system
- Actions may succeed after conflicts are resolved

### 8. Infinite Loop Prevention
- **Guard mechanism**: Maximum 1 message per sender→receiver pair per frame
- Prevents endless pushing cycles
- Prevents runaway chain reactions
- Enforced through banned sender/receiver tracking

## Architecture Components

### Command Pipeline (`app/bus/command_pipeline.py`)
```python
class ActorAction:
    actor: Actor              # Target actor
    behaviour: Behaviours     # Which behavior to invoke  
    method_name: str         # Specific behavior method
    args: tuple              # Method arguments
    attempts_number: int     # Retry tracking
```

**Key Features:**
- Queue-based action processing
- Recursive blocking action resolution
- Maximum recursion depth protection (5 levels)
- Retry mechanism with attempt limits

### Message Broker (`app/bus/message_brocker.py`)
```python
class Message:
    sender: Actor
    action: ActionFn
    receivers: ActorsCollection
    attempts_to_process: int

class Promise:
    # Placeholder for future promise-based resolution
```

**Key Features:**
- Actor-to-actor messaging system
- Promise-based conflict resolution (planned)
- Message attempt tracking

### Event Bus (`app/engine/state/event_bus.py`)
```python
class EventBus:
    _queue: Deque[Message]
    __banned: Dict[str, Banned]  # Sender→Receiver ban tracking
```

**Key Features:**
- Message queue processing
- Banned sender/receiver tracking with timestamps
- Conflict resolution through message re-queuing
- State change detection

## State Flow Diagram

```
Input → ActorAction → CommandPipeline → BehaviorMethod
                                           ↓
Grid Update ← StateChange ←────────────── Success
    ↓                                      ↑
 Success                                   │
                                          │
Conflict → Message → TargetActors → Promises → ReactionActions
    ↓         ↓                                      ↓
RollBack   BanList                           CommandPipeline
    ↓         ↓                                      ↓
Re-queue   TimeLimit                              Retry
```

## Implementation Status

### Implemented:
- ✅ ActorAction dataclass with behavior resolution
- ✅ CommandPipeline with recursive processing
- ✅ EventBus with message queuing and ban system
- ✅ Basic conflict detection and re-queuing
- ✅ Attempt limiting and recursion protection

### Planned/Incomplete:
- ⏳ Promise system for async conflict resolution  
- ⏳ Message broker integration with CommandPipeline
- ⏳ Grid-based conflict detection
- ⏳ State rollback mechanism
- ⏳ Journal-based event tracking
- ⏳ Integration with main game loop

## Design Principles

1. **Deterministic Resolution**: Same inputs always produce same outputs
2. **Conflict Isolation**: Failed actions don't corrupt system state
3. **Chain Reaction Control**: Prevent infinite interaction loops
4. **Temporal Consistency**: All frame-based interactions complete within frame boundaries
5. **Actor Autonomy**: Each actor manages its own behavior responses
6. **State Atomicity**: Actions either fully succeed or fully fail

## Future Considerations

- **Journal Integration**: Event logging for debugging and replay
- **Performance Optimization**: Batch processing for large actor counts  
- **Priority Systems**: Action ordering based on actor initiative/priority
- **Network Synchronization**: Deterministic resolution for multiplayer