from .frame_context import FrameContext
from .level_context import GridContext


class Context:
    _instance = None

    def __init__(self):
        self.frame_context: FrameContext = FrameContext()
        self.grid_context: GridContext = GridContext()

    @classmethod
    def instance(cls) -> "Context":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
