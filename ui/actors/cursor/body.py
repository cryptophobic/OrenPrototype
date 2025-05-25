from ui.actors.body import Body as BaseBody, CollisionMatrix
from ui.actors.cursor.shape import Shape


class Body(BaseBody):
    def __init__(self):
        super().__init__(
            collision_matrix=CollisionMatrix(block=False, overlap=True, ignore=False),
            shape=Shape()
        )
