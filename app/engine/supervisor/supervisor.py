class Supervisor:
    def __init__(self, state_manager=None):
        self.state_manager = state_manager
        self.mode = "turn_based"  # or "real_time"
        self.current_player = None

    def set_mode(self, mode: str):
        """Set game mode: 'turn_based' or 'real_time'"""
        self.mode = mode

    def activate_actor(self, actor_name: str):
        """Activate an actor by name"""
        if self.state_manager and actor_name in self.state_manager.actors:
            actor = self.state_manager.actors[actor_name]
            if hasattr(actor, 'active'):
                actor.active = True

    def deactivate_actor(self, actor_name: str):
        """Deactivate an actor by name"""
        if self.state_manager and actor_name in self.state_manager.actors:
            actor = self.state_manager.actors[actor_name]
            if hasattr(actor, 'active'):
                actor.active = False

    def switch_active_player(self, new_player: str):
        """Switch control to a different player"""
        if self.current_player:
            self.deactivate_actor(self.current_player)
        self.activate_actor(new_player)
        self.current_player = new_player

    def update(self):
        """Update supervisor logic - runs before state_manager.update_state()"""
        # Placeholder for turn-based logic or real-time AI activation
        # Will implement actual logic later
        pass