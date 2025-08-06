import arcade


class AnimatedTile(arcade.Sprite):
    def __init__(self, textures, frame_durations):
        super().__init__(textures[0])
        self.textures = textures
        self.frame_durations = frame_durations
        self.current_frame = 0
        self.time_accum = 0

    def update(self, delta_time: float = 1/60,  *args, **kwargs):
        self.time_accum += delta_time * 1000  # convert to ms
        if self.time_accum > self.frame_durations[self.current_frame]:
            self.time_accum = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures)
            self.texture = self.textures[self.current_frame]

