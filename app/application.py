import arcade

from app import config as cfg
from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.collections.puppeteer_collection import PuppeteerCollection
from app.config import Behaviours
from app.engine.command_pipeline.pipeline import CommandPipeline
from app.engine.context.game_context import GameContext
from app.engine.input_processor.InputEvents import InputEvents
from app.engine.input_processor.Timer import Timer
from app.engine.message_broker.broker import MessageBroker
from app.engine.message_broker.types import Message, MessageBody, MessageTypes, InputPayload
from app.maps.level1 import LevelFactory
from app.objects.coordinate_holder import CoordinateHolder
from app.objects.orchestrator import Orchestrator
from app.objects.puppeteer import Puppeteer
from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.objects.orchestrator_protocol import OrchestratorProtocol
from app.registry.behaviour_registry import get_behaviour_registry


class GameView(arcade.View):

    def __calculate_settings(self):

        screen_width, screen_height = self.config.SCREEN_SIZE

        tile_width = (screen_width - (self.grid.width + 1) * self.margin) // self.grid.width
        tile_height = (screen_height - (self.grid.height + 1) * self.margin) // self.grid.height

        self.tile_size = min(tile_width, tile_height)

        # Create a list of solid-color sprites to represent each grid location
        for row in range(self.grid.height):
            self.grid_sprites.append([])
            for column in range(self.grid.width):
                sprite = arcade.SpriteSolidColor(self.tile_size, self.tile_size, color=arcade.color.WHITE)
                sprite.center_x = self.get_tile_center(column)
                sprite.center_y = self.get_tile_center(row)
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

    def get_tile_center(self, index: int) -> int:
        return self.margin + (self.tile_size + self.margin) * index + self.tile_size // 2

    def register_actors(self):
        for puppeteer in self.orchestrator.actors_collection.get_by_type(Puppeteer, PuppeteerCollection):
            self.input_events.subscribe(puppeteer.name, puppeteer.controls)

    def __init__(self, config):
        super().__init__()

        self.config = config

        self.interval = 1000 / self.config.FPS

        self.level_factory = LevelFactory()
        self.current_level = self.level_factory.levels["level1"]
        self.grid = self.current_level.grid
        self.context = GameContext()
        self.input_events = InputEvents()
        self.message_broker = MessageBroker()

        self.orchestrator: OrchestratorProtocol = Orchestrator(self.current_level.actors_collection)
        self.orchestrator.behaviours.set(Behaviours.INPUT_HANDLER)

        self.command_pipeline = CommandPipeline()
        self.command_pipeline.actor_collection = self.orchestrator.actors_collection

        self.register_actors()

        base_behaviour = get_behaviour_registry().get(Behaviours.BEHAVIOUR)
        base_behaviour.register_grid(self.current_level.grid)
        base_behaviour.register_messenger(self.message_broker)

        # TODO: testing, debugging
        self.puppets = list(self.orchestrator.moveable_actors.raw_items().values())
        self.i = 0
        # EOF TODO

        self.ticker = Timer()
        self.state_changed = True

        self.x_offset: int = 0
        self.y_offset: int = 0
        self.tile_size: int = 0
        self.actor_collection: ActorCollectionProtocol = self.current_level.actors_collection
        self.background_color = arcade.color.BLACK
        self.margin = 2

        self.tile_size = 0
        self.grid_sprite_list = arcade.SpriteList()
        self.actor_sprite_list = arcade.SpriteList()
        self.cursor_sprite_list = arcade.SpriteList()

        self.grid_sprites = []
        self.actor_sprite_map = {}
        self.__calculate_settings()


    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.grid_sprite_list.draw()

        # We should always start by clearing the window pixels
        if self.state_changed:
            self.state_changed = False

            current_actor_ids = set()

            for coordinate_holder in self.actor_collection.get_by_type(CoordinateHolder, CoordinateHolderCollection):
                current_actor_ids.add(coordinate_holder.id)
                x = coordinate_holder.coordinates.x
                y = coordinate_holder.coordinates.y
                icon_path = coordinate_holder.shape.icon_path

                if coordinate_holder.name not in self.actor_sprite_map:
                    # Create and add new sprite
                    sprite = arcade.Sprite(icon_path, scale=self.tile_size / 16)
                    self.actor_sprite_map[coordinate_holder.name] = sprite
                    if coordinate_holder.name == "Cursor":
                        self.cursor_sprite_list.append(sprite)
                    else:
                        self.actor_sprite_list.append(sprite)
                else:
                    sprite = self.actor_sprite_map[coordinate_holder.name]

                sprite.center_x = self.get_tile_center(x)
                sprite.center_y = self.get_tile_center(y)

            # Remove sprites of actors that no longer exist
            to_remove = [actor_id for actor_id in self.actor_sprite_map if actor_id not in current_actor_ids]
            for actor_id in to_remove:
                sprite = self.actor_sprite_map.pop(actor_id)
                self.actor_sprite_list.remove(sprite)

        self.actor_sprite_list.draw()
        self.cursor_sprite_list.draw()

    def on_update(self, delta_time: float):
        current_timestamp = self.ticker.current_timestamp()
        render_threshold = int(self.ticker.last_timestamp + self.interval)
        self.input_events.listen(current_timestamp)
        if current_timestamp >= render_threshold:
            events = self.input_events.slice_flat(self.ticker.last_timestamp, render_threshold)
            self.ticker.tick()

            if not events:
                return

            # TODO: Maybe later move this logic to some behaviour as currently only behaviours sending messages
            message = Message(
                sender="Application",
                body=MessageBody(
                    message_type=MessageTypes.INPUT,
                    payload=InputPayload(events),
                )
            )
            _, pending_actions = self.message_broker.send_message(message, self.orchestrator)
            self.orchestrator.pending_actions.extend(pending_actions)

            # TODO: think twice if it is logical enough to pass self.orchestrator
            self.state_changed = self.command_pipeline.process(self.orchestrator)
            self.context.tick() # frame number increment

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            arcade.exit()

        if key == arcade.key.TAB:
            length = len(self.puppets)
            self.orchestrator.set_puppet(self.puppets[self.i % length].name)
            self.i += 1


        self.input_events.key_pressed[key] = True

    def on_key_release(self, key: int, modifiers: int):
        self.input_events.key_pressed.pop(key, None)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Convert the clicked mouse position into grid coordinates
        # column = int(x // (WIDTH + MARGIN))
        # row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: (?, ?)")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        # if row >= ROW_COUNT or column >= COLUMN_COUNT:
        #    # Simply return from this method since nothing needs updating
        #    return

        # Flip the color of the sprite
        # if self.grid_sprites[row][column].color == arcade.color.WHITE:
        #    self.grid_sprites[row][column].color = arcade.color.GREEN
        # else:
        #    self.grid_sprites[row][column].color = arcade.color.WHITE

class Application:
    def __init__(self):
        self.config = cfg

    def run(self):
        window = arcade.Window(self.config.SCREEN_SIZE[0], self.config.SCREEN_SIZE[1], "OrenPrototype - Arcade Version")

        game = GameView(self.config)
        window.show_view(game)
        arcade.run()
