import arcade

from app.core.vectors import CustomVec2f, CustomVec2i
from app.engine.game_view.animated_sprite import Animated


class Moving(Animated):
    def __init__(self, texture_list: list[arcade.Texture]):
        super().__init__(texture_list)
        self.buffer = CustomVec2f(0.0, 0.0)

    def stop_x(self):
        self.buffer.x = 0.0

    def stop_y(self):
        self.buffer.y = 0.0

    def stop(self):
        self.stop_x()
        self.stop_y()

    def update_movement(self, delta_time, velocity: CustomVec2f):
        self.buffer += velocity * delta_time

        moved = CustomVec2i(0, 0)

        if abs(self.buffer.x) >= 1:
            step = int(self.buffer.x)
            self.buffer.x -= step
            moved.x = step

        if abs(self.buffer.y) >= 1:
            step = int(self.buffer.y)
            self.buffer.y -= step
            moved.y = step

        return moved