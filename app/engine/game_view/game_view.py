import arcade
from arcade.types import Color

from app.behaviours.types import BufferedMoverState
from app.collections.puppeteer_collection import PuppeteerCollection
from app.config import Behaviours
from app.core.event_bus.bus import EventBus
from app.engine.command_pipeline.pipeline import CommandPipeline
from app.engine.game_view.camera import Camera
from app.engine.game_view.sprite_renderer import SpriteRenderer
from app.engine.game_view.tmx_animation_parser import load_animated_tilemap
from app.engine.input_processor.Timer import Timer
from app.engine.input_processor.inpuit_events_continuous import InputEventsContinuous
from app.engine.message_broker.broker import MessageBroker
from app.maps.level1 import LevelFactory
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
        self.tile_size = 16
        for row in range(self.grid.height):
            self.grid_sprites.append([])
            for column in range(self.grid.width):
                sprite = arcade.SpriteSolidColor(self.tile_size, self.tile_size, color=Color(0x1E, 0x51, 0x28, 255))
                sprite.center_x = self.get_tile_center(column)
                sprite.center_y = self.get_tile_center(row)
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

    def get_tile_center(self, index: int) -> int:
        return self.margin + (self.tile_size + self.margin) * index + self.tile_size // 2

    def register_actors(self):
        for puppeteer in self.orchestrator.actors_collection.get_by_type(Puppeteer, PuppeteerCollection):
            self.input_events_continuous.subscribe(puppeteer.name, puppeteer.controls)

    def __init__(self, config):
        super().__init__()

        self.margin = 0

        map_name = 'c:/Users/dmitr/PycharmProjects/OrenPrototype/app/resources/animations/tiles/Tiled_files/Glades.tmx'
        self.scene = load_animated_tilemap(tmx_file_path=map_name, scaling=1)

        self.camera = Camera(initial_zoom=1.0)

        self.config = config
        self.rendered = False

        self.interval = 1000 / self.config.FPS

        self.level_factory = LevelFactory()
        self.current_level = self.level_factory.levels["level1"]
        self.grid = self.current_level.grid

        self.input_events_continuous = InputEventsContinuous()
        self.message_broker = MessageBroker()
        self.event_bus = EventBus()

        self.orchestrator: OrchestratorProtocol = Orchestrator(
            self.current_level.actors_collection,
            self.message_broker,
            "Orchestrator")

        self.command_pipeline = CommandPipeline()
        self.command_pipeline.actor_collection = self.orchestrator.actors_collection

        self.register_actors()

        base_behaviour = get_behaviour_registry().get(Behaviours.BEHAVIOUR)
        base_behaviour.register_event_bus(self.event_bus)
        base_behaviour.register_grid(self.current_level.grid)
        base_behaviour.register_messenger(self.message_broker)

        # TODO: testing, debugging
        self.puppets = list(self.orchestrator.moveable_actors.raw_items().values())
        self.i = 0
        # EOF TODO

        self.ticker = Timer()
        self.state_changed = True

        self.actor_collection: ActorCollectionProtocol = self.current_level.actors_collection
        self.background_color = arcade.color.GRAY_ASPARAGUS

        self.tile_size = 0
        self.grid_sprite_list = arcade.SpriteList()
        self.grid_sprites = []
        
        self.__calculate_settings()
        self.sprite_renderer = SpriteRenderer(self.tile_size, self.get_tile_center)
        self.sprite_renderer.register_event_bus(self.event_bus)


    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.camera.use()

        self.grid_sprite_list.draw()
        self.scene.draw()

        # for x in range(self.grid.width):
        #     arcade.draw_line(16 * x, 0, 16 * x, 16 * 29, arcade.color.GRAY_ASPARAGUS, 0.5)

        # for y in range(self.grid.height):
        #     arcade.draw_line(0, 16 * y, 16 * 43, 16 * y, arcade.color.GRAY_ASPARAGUS, 0.5)


        if not self.rendered or self.state_changed:
            self.state_changed = False
            self.rendered = True
            self.sprite_renderer.update_sprites(self.actor_collection)

        self.sprite_renderer.draw()
        self.scene["objects1"].draw()
        self.scene["objects2"].draw()
        self.scene["objects3"].draw()


    def on_update(self, delta_time: float):
        current_timestamp = self.ticker.current_timestamp()
        render_threshold = int(self.ticker.last_timestamp + self.interval)
        self.input_events_continuous.listen(current_timestamp)
        if current_timestamp >= render_threshold:
            prev_timestamp = self.ticker.last_timestamp
            self.ticker.tick()
            last_timestamp = self.ticker.last_timestamp

            input_events = self.input_events_continuous.read(prev_timestamp, last_timestamp)

            self.orchestrator.process_tick(delta_time)
            self.orchestrator.process_continuous_input(input_events)

            self.state_changed = self.command_pipeline.process(
                self.orchestrator.actors_collection.get_pending_actors()
            )

        sprite = self.sprite_renderer.actor_sprite_map.get(self.orchestrator.puppeteer.puppet.name, None)
        if sprite:
            self.camera.set_follow_target(sprite, smooth=True, speed=0.1)

        state = self.orchestrator.puppeteer.puppet.extract_behaviour_data(Behaviours.BUFFERED_MOVER)
        if isinstance(state, BufferedMoverState):
            velocity = state.intent_velocity
            zoom = self.camera.zoom
            if velocity.is_not_zero():
                if zoom < 4.0:
                    zoom += 0.01
                self.camera.set_zoom(zoom)
            else:
                if zoom > 3.0:
                    zoom -= 0.1
                self.camera.set_zoom(zoom)

        self.camera.update()
        self.sprite_renderer.update()
        self.scene.update(delta_time=delta_time)

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            arcade.exit()

        # playground
        if key == arcade.key.TAB:
            length = len(self.puppets)
            self.orchestrator.set_puppet(self.puppets[self.i % length].name)
            self.i += 1

        current_timestamp = self.ticker.current_timestamp()
        self.input_events_continuous.register_key_pressed(key, True, current_timestamp)

    def on_key_release(self, key: int, modifiers: int):
        current_timestamp = self.ticker.current_timestamp()
        self.input_events_continuous.register_key_pressed(key, False, current_timestamp)
