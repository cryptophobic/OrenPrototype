from .level import Level
from ..helpers.vectors import Vec2
from ..objects.actor.static_object import StaticObject
from ..objects.actor.unit import Stats, Unit
from ..resources.index import get_icon, Icons
from ..objects.actor.body import Body, CollisionMatrix, CollisionResponse
from ..objects.actor.coordinate_holder import CoordinateHolder
from ..objects.actor.shape import Shape

class LevelFactory:
    def __init__(self):
        level = Level()
        level.grid_width = 30
        level.grid_height = 25

        # Cursor init
        cursor_body = Body(CollisionMatrix(response=CollisionResponse.OVERLAP))
        cursor_shape = Shape(get_icon(Icons.CURSOR))
        level.coordinate_holders.add(CoordinateHolder(body=cursor_body, shape=cursor_shape, coordinates=Vec2(2, 1), name="Cursor"))
        # End of Cursor init

        # Player init
        player_body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
        player_shape = Shape(get_icon(Icons.PLAYER))
        player_stats = Stats(STR=5, DEX=1, CON=5, INT=2, WIS=2, CHA=1, HP=10, initiative=1)
        level.coordinate_holders.add(Unit(body=player_body, shape=player_shape, coordinates=Vec2(0, 0), stats=player_stats, name="Adventurer"))
        # End of player init

        # Prison walls
        for coordinates in [Vec2(1, 0), Vec2(1, 1), Vec2(0, 1)]:
            prison_body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
            prison_shape = Shape(get_icon(Icons.WALLS))
            # Unique name would be created automatically.
            level.static_objects.add(StaticObject(
                body=prison_body,
                shape=prison_shape,
                coordinates=coordinates,
                height=100,
                weight=100,
            ))
        # End of prison walls

        self.levels = { "level1": level }
