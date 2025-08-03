import arcade

from app.config import CommonAnimations


class Animated(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture], animation: CommonAnimations):
        super().__init__(texture_list[0])
        self.time_elapsed = 0
        self.textures = []
        self.animation = None
        self.frames = 0
        self.set_animation(texture_list, animation)

    def set_animation(self, texture_list: list[arcade.Texture], animation: CommonAnimations) -> None:
        self.textures = texture_list
        self.animation = animation
        self.frames = len(texture_list)
        self.cur_texture_index = self.cur_texture_index % self.frames

    def update(self, delta_time: float = 1/60,  *args, **kwargs) -> None:
        self.time_elapsed += delta_time

        if self.time_elapsed > 0.1:
            self.time_elapsed = 0
            self.set_texture(self.cur_texture_index)
            self.cur_texture_index = (self.cur_texture_index + 1) % self.frames
