import arcade


from app.engine.game_view.tmx_animation_parser import load_animated_tilemap

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SCREEN_TITLE = "TMX Example"


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        map_name = 'c:/Users/dmitr/PycharmProjects/OrenPrototype/app/resources/animations/tiles/Tiled_files/Glades.tmx'
        scaling = 1.4

        # Optional: choose which layers should use spatial hash for collisions
        layer_options = {
            "Walls": {"use_spatial_hash": True},
        }

        # Load animated tilemap using factory
        self.scene = load_animated_tilemap(
            map_name, scaling, layer_options
        )

        # Camera for scrolling/zoom
        self.camera = arcade.Camera2D()

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

    def on_update(self, delta_time: float):
        self.scene.update(delta_time=delta_time)

def tmx_loader():
    game = MyGame()
    arcade.run()
