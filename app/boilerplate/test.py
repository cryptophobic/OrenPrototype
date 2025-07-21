"""
Array Backed Grid Shown By Sprites

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

This version makes a grid of sprites instead of numbers. Instead of
iterating all the cells when the grid changes we simply just
swap the color of the selected sprite. This means this version
can handle very large grids and still have the same performance.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid_sprites_2
"""
import arcade
from PIL import Image
from arcade import Texture

from app.collections.animation_collection import AnimationCollection
from app.config import NpcAnimations
from app.core.vectors import CustomVec2i, CustomVec2f
from app.protocols.collections.animation_collection_protocol import AnimationCollectionProtocol

# Set how many rows and columns we will have
ROW_COUNT = 30
COLUMN_COUNT = 30

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 32
HEIGHT = 32

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

CELL_WIDTH = 1.0  # logical cell size
VELOCITY_PER_CELL_150MS = 1 / 0.5  # ~6.67 cells/sec
VELOCITY_PER_CELL_300MS = 1 / 0.25


# Do the math to figure out our screen dimensions
WINDOW_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
WINDOW_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
WINDOW_TITLE = "Array Backed Grid Buffered Example"

class Player(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture]):
        super().__init__(texture_list[0])
        self.time_elapsed = 0
        self.coordinates: CustomVec2i = CustomVec2i(12, 14)
        self.velocity: CustomVec2f = CustomVec2f.zero()
        self.buffer: CustomVec2f = CustomVec2f(0.0, 0.0)
        self.cell_size = 1.0

        self.textures = texture_list

    def update(self, delta_time: float = 1/60,  *args, **kwargs) -> None:
        self.time_elapsed += delta_time

        if self.time_elapsed > 0.1:
            self.time_elapsed = 0
            self.set_texture(self.cur_texture_index)
            self.cur_texture_index = (self.cur_texture_index + 1) % 5


    def update_movement(self, delta_time, keys_held):
        self.buffer += self.velocity * delta_time
        moved = [self.buffer.x == 0, self.buffer.y == 0]

        if abs(self.buffer.x) >= self.cell_size:
            sign = 1 if self.buffer.x >= 0 else -1
            step = sign * int(abs(self.buffer.x) // self.cell_size)
            self.coordinates.x += step
            self.buffer.x -= step * self.cell_size
            moved[0] = True

        if abs(self.buffer.y) >= self.cell_size:
            sign = 1 if self.buffer.y >= 0 else -1
            step = sign * int(abs(self.buffer.y) // self.cell_size)
            self.coordinates.y += step
            self.buffer.y -= step * self.cell_size
            moved[1] = True

        if moved[0] and self.velocity.x:
            # Refresh velocity if key still held
            vx = 0.0
            if arcade.key.RIGHT in keys_held:
                vx += VELOCITY_PER_CELL_150MS
            if arcade.key.LEFT in keys_held:
                vx -= VELOCITY_PER_CELL_150MS
            self.velocity.x = vx

            if vx == 0:
                # Stop at cell if no input
                self.buffer.x = 0.0

        if moved[1] and self.velocity.y:
            # Refresh velocity if key still held
            vy = 0.0
            if arcade.key.UP in keys_held:
                vy += VELOCITY_PER_CELL_300MS
            if arcade.key.DOWN in keys_held:
                vy -= VELOCITY_PER_CELL_300MS
            self.velocity.y = vy

            if vy == 0:
                # Stop at cell if no input
                self.buffer.y = 0.0


def slice_animation_strip(image_path: str, start_x: int, start_y: int, frame_width: int, frame_height: int, count: int) -> list[Texture]:
    pil_image = Image.open(image_path)
    frames = []
    for i in range(count):
        box = (
            start_x + i * frame_width,
            start_y,
            start_x + (i + 1) * frame_width,
            start_y + frame_height
        )
        cropped = pil_image.crop(box).convert("RGBA")
        tex = Texture(name=f"frame_{i}", image=cropped)
        frames.append(tex)
    return frames

class GameView(arcade.View):
    """
    Main application class.
    """
    def get_tile_center(self, index: int) -> int:
        return MARGIN + (WIDTH + MARGIN) * index + WIDTH // 2

    def get_tile_index_from_pixel(self, pixel: CustomVec2i) -> CustomVec2i:
        return CustomVec2i(
            (pixel.x - MARGIN) // (WIDTH + MARGIN),
            (pixel.y - MARGIN) // (HEIGHT + MARGIN),
        )

    def __init__(self):
        super().__init__()
        self.grid_sprite_list = arcade.SpriteList()
        self.grid_sprites = []
        self.rocks = []

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            for column in range(COLUMN_COUNT):
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, color=arcade.color.WHITE)

                sprite.center_x = self.get_tile_center(column)
                sprite.center_y = self.get_tile_center(row)
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

        self.sprite_list = arcade.SpriteList()
        self.background_color = arcade.color.GRAY_ASPARAGUS

        self.animations: AnimationCollectionProtocol = AnimationCollection()
        self.animations.set(NpcAnimations.ARMED_RUN)

        # frames = slice_animation_strip("resources/craftpix/male/PNG/Sword_attack/Sword_attack_full.png",
        #                               0, 0, 64, 64, 8)

        self.keys_held = set()
        self.player = Player(self.animations.get(NpcAnimations.ARMED_RUN).front)
        self.player.scale = 1.0
        self.player.position = self.get_tile_center(self.player.coordinates.x), self.get_tile_center(self.player.coordinates.y)

        self.sprite_list.append(self.player)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

        if symbol in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.keys_held.add(symbol)
            if symbol == arcade.key.UP:
                self.player.velocity.y = VELOCITY_PER_CELL_300MS
            elif symbol == arcade.key.DOWN:
                self.player.velocity.y = -VELOCITY_PER_CELL_300MS
            elif symbol == arcade.key.RIGHT:
                self.player.velocity.x = VELOCITY_PER_CELL_150MS
            elif symbol == arcade.key.LEFT:
                self.player.velocity.x = -VELOCITY_PER_CELL_150MS

    def on_key_release(self, symbol, modifiers):
        self.keys_held.discard(symbol)

    def on_update(self, delta_time: float) -> bool | None:
        self.player.update_movement(delta_time, self.keys_held)

        start_x = self.get_tile_center(self.player.coordinates.x) + self.player.buffer.x * WIDTH
        start_y = self.get_tile_center(self.player.coordinates.y) + self.player.buffer.y * HEIGHT

        # Update sprite position based on grid coordinates
        self.player.center_x = start_x
        self.player.center_y = start_y
        self.grid_sprites[self.player.coordinates.y][self.player.coordinates.x].color = arcade.color.RUST
        normalized = CustomVec2f(start_x, start_y) + CustomVec2f(self.player.velocity.x,
                                                                 self.player.velocity.y).normalized().scale_to(WIDTH)

        index = self.get_tile_index_from_pixel(normalized)
        self.grid_sprites[index.y][index.x].color = arcade.color.GRANNY_SMITH_APPLE

        self.sprite_list.update()


    def on_draw(self):
        self.clear()
        self.grid_sprite_list.draw()
        self.sprite_list.draw()

        start_x = self.get_tile_center(self.player.coordinates.x) + self.player.buffer.x * WIDTH
        start_y = self.get_tile_center(self.player.coordinates.y) + self.player.buffer.y * HEIGHT

        # Scale vector visually (e.g., exaggerate length for clarity)
        normalized = CustomVec2f(start_x, start_y) + CustomVec2f(self.player.velocity.x, self.player.velocity.y).normalized().scale_to(WIDTH)

        arcade.draw_line(start_x, start_y, normalized.x, normalized.y, arcade.color.BLUE, 2)


def boilerplate():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create the GameView
    game = GameView()

    # Show GameView on the screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()
