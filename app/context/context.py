from .actors_collection import ActorsCollection
from .frame_context import FrameContext
from .grid_context import GridContext
from ..maps.level import Level


class Context:
    _instance = None

    def __init__(self):
        self.frame_context: FrameContext = FrameContext()
        self.grid_context: GridContext = GridContext()
        self.actors_collection: ActorsCollection = ActorsCollection()

    def init_from_level(self, level: Level):
        self.grid_context.load_grid(level.grid_height, level.grid_width)
        for coordinate_holder in level.coordinate_holders:
            self.actors_collection.add_actor(coordinate_holder)
            self.grid_context.grid.place_unit(coordinate_holder)

    @classmethod
    def instance(cls) -> "Context":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
