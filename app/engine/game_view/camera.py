import arcade
from typing import Optional


class Camera(arcade.Camera2D):
    """Game camera that extends arcade.Camera2D with tactical game-specific features."""
    
    def __init__(self, initial_zoom: float = 1.0):
        super().__init__()
        self.zoom = initial_zoom
        self._follow_target: Optional[arcade.Sprite] = None
        self._follow_smooth: bool = True
        self._follow_speed: float = 0.1
        
    def set_follow_target(self, sprite: Optional[arcade.Sprite], smooth: bool = True, speed: float = 0.1):
        """Set a sprite for the camera to follow.
        
        Args:
            sprite: The sprite to follow, or None to stop following
            smooth: Whether to smoothly interpolate to the target position
            speed: Interpolation speed when smooth=True (0.0 to 1.0)
        """
        self._follow_target = sprite
        self._follow_smooth = smooth
        self._follow_speed = max(0.0, min(1.0, speed))
        
    def center_on_sprite(self, sprite: arcade.Sprite):
        """Immediately center the camera on a sprite."""
        self.position = (sprite.center_x, sprite.center_y)
        
    def center_on_position(self, x: float, y: float):
        """Immediately center the camera on a position."""
        self.position = (x, y)
        
    def update(self):
        """Update camera position if following a target."""
        if self._follow_target is None:
            return
            
        target_x = self._follow_target.center_x
        target_y = self._follow_target.center_y
        
        if self._follow_smooth:
            current_x, current_y = self.position
            new_x = current_x + (target_x - current_x) * self._follow_speed
            new_y = current_y + (target_y - current_y) * self._follow_speed
            self.position = (new_x, new_y)
        else:
            self.position = (target_x, target_y)
            
    def set_zoom(self, zoom_level: float):
        """Set camera zoom level."""
        self.zoom = max(0.1, zoom_level)
        
    def adjust_zoom(self, delta: float):
        """Adjust zoom by a delta amount."""
        self.set_zoom(self.zoom + delta)
        
    def get_viewport_bounds(self) -> tuple[float, float, float, float]:
        """Get the current viewport bounds in world coordinates.
        
        Returns:
            tuple: (left, bottom, right, top) bounds
        """
        center_x, center_y = self.position
        half_width = (self.viewport_width / 2) / self.zoom
        half_height = (self.viewport_height / 2) / self.zoom
        
        return (
            center_x - half_width,  # left
            center_y - half_height,  # bottom
            center_x + half_width,   # right
            center_y + half_height   # top
        )