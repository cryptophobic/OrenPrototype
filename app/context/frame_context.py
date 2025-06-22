class FrameContext:
    _instance = None

    def __init__(self):
        self.timestamp: int = 0

    @classmethod
    def instance(cls) -> "FrameContext":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
