class GameContext:
    def __init__(self):
        self.frame_number = 0

    def tick(self) -> None:
        self.frame_number += 1
