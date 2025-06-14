from deprecated.ui.actors.body import Body as BaseBody, CollisionMatrix, CollisionResponse
from deprecated.ui.actors.cursor.shape import Shape


class Body(BaseBody):
    def __init__(self):
        super().__init__(
            collision_matrix=CollisionMatrix(response=CollisionResponse.OVERLAP),
            shape=Shape()
        )
