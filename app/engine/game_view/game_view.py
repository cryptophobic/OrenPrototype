import arcade

from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.collections.puppeteer_collection import PuppeteerCollection
from app.config import Behaviours
from app.engine.command_pipeline.pipeline import CommandPipeline
from app.engine.game_view.animated_sprite import Animated
from app.engine.input_processor.InputEvents import InputEvents
from app.engine.input_processor.Timer import Timer
from app.engine.input_processor.inpuit_events_continuous import InputEventsContinuous
from app.engine.message_broker.broker import MessageBroker
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

        for row in range(self.grid.height):
            self.grid_sprites.append([])
            for column in range(self.grid.width):
                sprite = arcade.SpriteSolidColor(self.tile_size, self.tile_size, color=arcade.color.GRAY_ASPARAGUS)
                sprite.center_x = self.get_tile_center(column)
                sprite.center_y = self.get_tile_center(row)
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

    def get_tile_center(self, index: int) -> int:
        return self.margin + (self.tile_size + self.margin) * index + self.tile_size // 2

    def register_actors(self):
        for puppeteer in self.orchestrator.actors_collection.get_by_type(Puppeteer, PuppeteerCollection):
            self.input_events_continuous.subscribe(puppeteer.name, puppeteer.controls)

            # TODO: Deprecated
            self.input_events.subscribe(puppeteer.name, puppeteer.controls)

    def __init__(self, config):
        super().__init__()

        self.config = config
        self.rendered = False

        self.interval = 1000 / self.config.FPS

        self.level_factory = LevelFactory()
        self.current_level = self.level_factory.levels["level1"]
        self.grid = self.current_level.grid
        self.input_events = InputEvents()
        self.input_events_continuous = InputEventsContinuous()
        self.message_broker = MessageBroker()

        self.orchestrator: OrchestratorProtocol = Orchestrator(
            self.current_level.actors_collection,
            self.message_broker,
            "Orchestrator")

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
        if not self.rendered or self.state_changed:
            self.state_changed = False
            self.rendered = True

            current_actor_ids = set()

            for coordinate_holder in self.actor_collection.get_by_type(CoordinateHolder, CoordinateHolderCollection):
                current_actor_ids.add(coordinate_holder.id)
                x = coordinate_holder.coordinates.x
                y = coordinate_holder.coordinates.y

                if coordinate_holder.name not in self.actor_sprite_map:

                    if len(coordinate_holder.shape.animations) == 0:
                        icon_path = coordinate_holder.shape.icon_path
                        sprite = arcade.Sprite(icon_path, scale=self.tile_size / 16)
                    else:
                        # TODO: just for testing purpose
                        current_animation_index = next(iter(coordinate_holder.shape.animations))
                        current_animation = coordinate_holder.shape.animations.get(current_animation_index).front
                        sprite = Animated(current_animation)

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
        self.input_events_continuous.listen(current_timestamp)
        if current_timestamp >= render_threshold:
            events = self.input_events.slice_flat(self.ticker.last_timestamp, render_threshold)
            check = self.input_events_continuous.read(self.ticker.last_timestamp, render_threshold)

            self.ticker.tick()
            self.orchestrator.process_tick(delta_time)
            self.orchestrator.process_input(events)
            self.state_changed = self.command_pipeline.process(
                self.orchestrator.actors_collection.get_pending_actors()
            )

        self.actor_sprite_list.update()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            arcade.exit()

        if key == arcade.key.TAB:
            length = len(self.puppets)
            self.orchestrator.set_puppet(self.puppets[self.i % length].name)
            self.i += 1

        current_timestamp = self.ticker.current_timestamp()
        self.input_events_continuous.register_key_pressed(key, True, current_timestamp)

        # TODO: deprecated
        self.input_events.key_pressed[key] = True

    def on_key_release(self, key: int, modifiers: int):
        current_timestamp = self.ticker.current_timestamp()
        self.input_events_continuous.register_key_pressed(key, False, current_timestamp)

        # TODO: deprecated
        self.input_events.key_pressed.pop(key, None)
