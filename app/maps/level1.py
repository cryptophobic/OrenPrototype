import pygame

from .level import Level
from ..bus.message_broker.types import MessageBody, MessageTypes, IntentionToMovePayload
from ..config import Behaviours
from ..helpers.vectors import Vec2
from ..objects.actor.puppeteer import Puppeteer, Controls, KeyBinding
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

        # Cursor setup
        cursor_body = Body(CollisionMatrix(response=CollisionResponse.OVERLAP))
        cursor_shape = Shape(get_icon(Icons.CURSOR))
        level.coordinate_holders.add(CoordinateHolder(body=cursor_body, shape=cursor_shape, coordinates=Vec2(2, 1), name="Cursor"))
        # End of Cursor setup

        # Player setup
        player_body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
        player_shape = Shape(get_icon(Icons.PLAYER))
        player_stats = Stats(STR=5, DEX=1, CON=5, INT=2, WIS=2, CHA=1, HP=10, initiative=1)
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

        self.levels = { "level1": level }
