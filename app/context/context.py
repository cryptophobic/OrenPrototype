from .actors_context import ActorsContext
from .frame_context import FrameContext
from .grid_context import GridContext
from ..maps.level import Level
from ..objects.actors_collection import ActorsCollection


class Context:
    _instance = None

    # Some actors couldn't be loaded within level.
    def __init__(self, actors_collection: ActorsCollection = None):
        self.frame_context: FrameContext = FrameContext()
        self.grid_context: GridContext = GridContext()
        self.actors_context: ActorsContext = ActorsContext(actors_collection or ActorsCollection())

    def init_from_level(self, level: Level):
        self.grid_context.load_grid(level.grid_height, level.grid_width)
        for name, coordinate_holder in level.coordinate_holders.items():
            self.actors_context.add_actor(coordinate_holder)
            self.grid_context.grid.place_coordinate_holder(coordinate_holder)

        for name, static_object in level.static_objects.items():
            self.actors_context.add_actor(static_object)
            self.grid_context.grid.place_coordinate_holder(static_object)

    @classmethod
    def instance(cls) -> "Context":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
