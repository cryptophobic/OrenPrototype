import arcade

from app import config as cfg
from app.engine.game_view.game_view import GameView


class Application:
    def __init__(self):
        self.config = cfg

    def run(self):
        window = arcade.Window(self.config.SCREEN_SIZE[0], self.config.SCREEN_SIZE[1], "OrenPrototype - Arcade Version")

        game = GameView(self.config)
        window.show_view(game)
        arcade.run()
