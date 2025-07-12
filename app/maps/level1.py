import pygame

from app.config import Behaviours
from app.core.geometry.shape import Shape
from app.core.physics.body import Body, CollisionMatrix, CollisionResponse
from app.core.vectors import Vec2
from app.engine.grid.grid import Grid
from app.engine.message_broker.types import Controls, KeyBinding, MessageBody, MessageTypes, IntentionToMovePayload
from app.maps.level import Level
from app.objects.coordinate_holder import CoordinateHolder
from app.objects.puppeteer import Puppeteer
from app.objects.static_object import StaticObject
from app.objects.types import UnitStats
from app.objects.unit import Unit
from app.resources.index import get_icon, Icons


class LevelFactory:
    def __init__(self):
        level = Level()
        level.grid_width = 30
        level.grid_height = 25

        level.grid = Grid(width=30, height=25)

        # Cursor setup
        cursor_body = Body(CollisionMatrix(response=CollisionResponse.OVERLAP))
        cursor_shape = Shape(get_icon(Icons.CURSOR))

        cursor_actor = CoordinateHolder(
            body=cursor_body,
            shape=cursor_shape,
            coordinates=Vec2(2, 1),
            name="Cursor")
        level.coordinate_holders.add(cursor_actor)
        # End of Cursor setup

        # Player setup
        player_body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
        player_shape = Shape(get_icon(Icons.PLAYER))
        player_stats = UnitStats(STR=5, DEX=1, CON=5, INT=2, WIS=2, CHA=1, HP=10, initiative=1)
        unit = Unit(body=player_body, shape=player_shape, coordinates=Vec2(0, 0), stats=player_stats, name="Adventurer")
        unit.add_behaviour_from_enum(Behaviours.MOVEABLE)
        level.coordinate_holders.add(unit)
        # End of player setup

        # Puppeteer setup
        controls = Controls()
        controls[pygame.K_UP] = KeyBinding(key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE, payload=IntentionToMovePayload(Vec2.up())))
        controls[pygame.K_DOWN] = KeyBinding(key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE, payload=IntentionToMovePayload(Vec2.down())))
        controls[pygame.K_LEFT] = KeyBinding(key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE, payload=IntentionToMovePayload(Vec2.left())))
        controls[pygame.K_RIGHT] = KeyBinding(key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE, payload=IntentionToMovePayload(Vec2.right())))

        puppeteer = Puppeteer(puppet=unit, controls=controls)
        puppeteer.add_behaviour_from_enum(Behaviours.POSSESSOR)
        # End of Puppeteer setup

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

        for coordinate_holder in level.coordinate_holders:
            level.actors_collection.add(coordinate_holder)
            level.grid.place(coordinate_holder, coordinate_holder.coordinates)

        for static_object in level.static_objects:
            level.actors_collection.add(static_object)
            level.grid.place(static_object, static_object.coordinates)


        self.levels = { "level1": level }
