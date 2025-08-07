import arcade

DEFAULT_ANIMATION_RATE = 100

class AnimatedSprite(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture], scale=1.0, frame_durations: list[float] = None):
        super().__init__(texture_list[0], scale)
        self.time_elapsed = 0
        self.textures = []
        self.frames = 0
        self.frame_durations = []
        self.set_animation(texture_list, frame_durations)

    def set_animation(self, texture_list: list[arcade.Texture], frame_durations: list[float] = None) -> None:
        self.textures = texture_list
        self.frames = len(texture_list)
        self.frame_durations = frame_durations if frame_durations is not None else []
        if len(self.frame_durations) != self.frames:
            self.frame_durations = [DEFAULT_ANIMATION_RATE] * self.frames

        self.cur_texture_index = self.cur_texture_index % self.frames

    def update(self, delta_time: float = 1/60,  *args, **kwargs) -> None:
        self.time_elapsed += delta_time * 1000

        if self.time_elapsed > self.frame_durations[self.cur_texture_index]:
            self.time_elapsed = 0
            self.set_texture(self.cur_texture_index)
            self.cur_texture_index = (self.cur_texture_index + 1) % self.frames
