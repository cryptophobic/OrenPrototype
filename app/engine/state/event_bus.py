from collections import deque
from typing import Callable


class EventBus:
    def __init__(self, grid=None):
        self.grid = grid
        self.action_queue = deque()

    def post(self, actor, action: Callable):
        """Add action to the queue"""
        self.action_queue.append((actor, action))

    def process_actions(self) -> bool:
        """Process all queued actions and return True if any state changes occurred"""
        state_changed = False
        
        while self.action_queue:
            actor, action = self.action_queue.popleft()
            try:
                # Execute the action
                if callable(action):
                    result = action()
                    if result:
                        state_changed = True
            except Exception as e:
                print(f"Error executing action for {getattr(actor, 'name', 'unknown')}: {e}")
        
        return state_changed

    def handle_movement_conflict(self, actor, target_cell):
        """Handle movement conflicts with 'pushed by' mechanics"""
        # Placeholder for conflict resolution
        # Will implement height-based collision and push mechanics
        pass

    def clear_queue(self):
        """Clear all pending actions"""
        self.action_queue.clear()