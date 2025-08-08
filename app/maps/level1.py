import arcade
from PIL.ImageCms import Direction

from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.config import Behaviours, NpcAnimations, animation_paths
from app.core.geometry.shape import Shape
from app.core.physics.body import Body, CollisionMatrix, CollisionResponse
from app.core.vectors import CustomVec2i
from app.engine.grid.grid import Grid
from app.engine.message_broker.types import Controls, KeyBinding, MessageBody, MessageTypes, IntentionToPlacePayload, \
    StopPayload, MovePayload
from app.maps.level import Level
from app.objects.coordinate_holder import CoordinateHolder
from app.objects.puppeteer import Puppeteer
from app.objects.static_object import StaticObject
from app.objects.types import UnitStats
from app.objects.unit import Unit
from app.protocols.objects.unit_protocol import UnitProtocol
from app.registry.icon_registry import get_icon_path, Icons


def maze(width, height):
    walls = "111111111111111111111111111111111111111111111111111100000000010000000100000000000100000100010000000001111111111010111010111010111111101110101010111011111100000100010001010000010100000101010001000101000001101011101111101011111111101110101011111111101111101101000001000101010000000000010101000001000000000101101111111011101010111111111110101011101111101010101100010000010001000100000000010100010100000101010101111010111010111111101111111010111110111110111010101101010100010001010001000001010001000100000000010101101010111111101010111011101010101110101111111111101101010100000101010001010001000100000100010001000101101010101010101011101110111110111110111010101010101100010101010100010100010100000100010100010100010001101110101010111010111010101111101011101110111111101101000001010100010100010000000101000001010001010001101110111011101110101011111110101111111011101010111100010001000000000101010000010101000000000101000101111011101111111111101010111011101011111110101011101100010000010000010001010101010001000000010101000101101111111110111010111010101010111011111011101110101100010000000100010100010001010100000001000101000101111010101111101110101111101010111111111110101011101101010101000101000101000001000100000000000101010001101010111010101110111011111111101111101111101011101100010001010100000100010000000100010001000001000101101110101010111111101111111010111010111011111110101101000100010100000001000000010100010001010000010101101011111110101111111010111110101111111010111010101101010000000100010001010000010001000001010001000001101010111111111010101111111010111011101010111111111101010000000001000100010000010100010100010100000001101111111110101111111010111011101110101111101111101101000100010101000001010100010001000001000001000101101010101011101011101010101110111111101011111011101100010001000101010001000100010000000101000100000101111111111110101010101110111111111110111110111110101101000100000100010101000100000000010000010100000101101010101111101110101011101111111010111010101011101100010100010100010101010001000001010101000001010001101110111010111010111010111011101010101111111110101101010000010001010000010001010001010000010000010101101011111110111011111111101010111011111010111010111101000001000100010000000100010101000001010100010001101011101010101111111010111110101111101110101110101101010001010000000001010100000100010100000100010101101010111111111111101110101111101010111111111011101100010100000100000000010101010001000000010001000001111110111010101111111010101010101111111010111111101100010001010101000001000101000100000001000100000001101011101010101011101110101111101111101011101111111101000101010101010100010101000100010101010001010001111110101010101010111011101010111010101010111010101100000101010101010000000001010001000101010001000101101110101010111011111110111011101111101111101111101100010100010001000000010100010101000100000100000101101010111111101111111011101110101010111011111110101101010000000101000001000000000101010000010000010101101011111111101011101111111111101011111110111010101101000000000000010000000000000001000000000001000001111111111111111111111111111111111111111111111111111"
    index = 0
    for x in range(width):
        for y in range(height):
            if walls[index] == '1':
                coordinates = CustomVec2i(x, y)
                prison_body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
                prison_shape = Shape(get_icon_path(Icons.WALLS))
                prison = StaticObject(
                    body=prison_body,
                    shape=prison_shape,
                    coordinates=coordinates,
                    height=100,
                    weight=100,
                )
                yield prison
            index += 1


class LevelFactory:
    def __init__(self):
        level = Level()
        level.grid_width = 43
        # level.grid_height = 51
        level.grid_height = 29

        level.grid = Grid(width=level.grid_width, height=level.grid_height)

        # Cursor setup
        # cursor_body = Body(CollisionMatrix(response=CollisionResponse.OVERLAP))
        # cursor_shape = Shape(get_icon_path(Icons.CURSOR))
        # cursor_actor = CoordinateHolder(
        #     body=cursor_body,
        #     shape=cursor_shape,
        #     coordinates=CustomVec2i(4, 8),
        #     name="Cursor")
        # cursor_actor.add_behaviour(Behaviours.DISCRETE_MOVER)
        # level.actors_collection.add(cursor_actor)
        # End of Cursor setup

        # Player setup
        player_body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
        player_shape = Shape(get_icon_path(Icons.PLAYER))
        player_shape.animations.set(animation_paths[NpcAnimations.ARMED_IDLE].animation, NpcAnimations.ARMED_IDLE)
        player_shape.animations.set(animation_paths[NpcAnimations.ARMED_RUN].animation, NpcAnimations.ARMED_RUN)
        player_shape.animations.set(animation_paths[NpcAnimations.ARMED_HURT].animation, NpcAnimations.ARMED_HURT)
        player_shape.animations.set(animation_paths[NpcAnimations.ARMED_WALK].animation, NpcAnimations.ARMED_WALK)
        player_shape.animations.set(animation_paths[NpcAnimations.ARMED_DEATH].animation, NpcAnimations.ARMED_DEATH)
        player_shape.animations.set(animation_paths[NpcAnimations.ARMED_ATTACK].animation, NpcAnimations.ARMED_ATTACK)
        player_shape.animations.set(animation_paths[NpcAnimations.ARMED_RUN_ATTACK].animation, NpcAnimations.ARMED_RUN_ATTACK)
        player_shape.animations.set(animation_paths[NpcAnimations.ARMED_WALK_ATTACK].animation, NpcAnimations.ARMED_WALK_ATTACK)

        player_stats = UnitStats(STR=5, DEX=1, CON=5, INT=2, WIS=2, CHA=1, HP=10, initiative=1)
        unit: UnitProtocol = Unit(body=player_body, shape=player_shape, coordinates=CustomVec2i(31, 19), stats=player_stats, name="Adventurer")
        unit.add_behaviour(Behaviours.DISCRETE_MOVER)
        unit.add_behaviour(Behaviours.BUFFERED_MOVER)
        level.actors_collection.add(unit)
        # End of player setup

        # Enemy setup
        enemy_body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
        enemy_shape = Shape(get_icon_path(Icons.ENEMY))
        enemy_shape.animations.set(animation_paths[NpcAnimations.ENEMY_IDLE].animation, NpcAnimations.ENEMY_IDLE)
        enemy_shape.animations.set(animation_paths[NpcAnimations.ENEMY_RUN].animation, NpcAnimations.ENEMY_RUN)
        enemy_shape.animations.set(animation_paths[NpcAnimations.ENEMY_HURT].animation, NpcAnimations.ENEMY_HURT)
        enemy_shape.animations.set(animation_paths[NpcAnimations.ENEMY_WALK].animation, NpcAnimations.ENEMY_WALK)
        enemy_shape.animations.set(animation_paths[NpcAnimations.ENEMY_DEATH].animation, NpcAnimations.ENEMY_DEATH)
        enemy_shape.animations.set(animation_paths[NpcAnimations.ENEMY_ATTACK].animation, NpcAnimations.ENEMY_ATTACK)
        enemy_shape.animations.set(animation_paths[NpcAnimations.ENEMY_RUN_ATTACK].animation, NpcAnimations.ENEMY_RUN_ATTACK)
        enemy_shape.animations.set(animation_paths[NpcAnimations.ENEMY_WALK_ATTACK].animation, NpcAnimations.ENEMY_WALK_ATTACK)
        enemy_stats = UnitStats(STR=5, DEX=1, CON=5, INT=2, WIS=2, CHA=1, HP=10, initiative=1)
        enemy_unit = Unit(body=enemy_body, shape=enemy_shape, coordinates=CustomVec2i(21, 18), stats=enemy_stats, name="Enemy")
        enemy_unit.add_behaviour(Behaviours.DISCRETE_MOVER)
        enemy_unit.add_behaviour(Behaviours.BUFFERED_MOVER)
        level.actors_collection.add(enemy_unit)
        # End of player setup

        # Puppeteer setup
        controls = Controls()
        controls[arcade.key.UP] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_PLACE, payload=IntentionToPlacePayload(CustomVec2i.up())),
            repeat_delta=150
        )
        controls[arcade.key.DOWN] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_PLACE, payload=IntentionToPlacePayload(CustomVec2i.down())),
            repeat_delta=150
        )
        controls[arcade.key.LEFT] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_PLACE, payload=IntentionToPlacePayload(CustomVec2i.left())),
            repeat_delta=150
        )
        controls[arcade.key.RIGHT] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_PLACE, payload=IntentionToPlacePayload(CustomVec2i.right())),
            repeat_delta=150
        )

        controls[arcade.key.W] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE, payload=MovePayload(direction=CustomVec2i.up())),
            key_up=MessageBody(message_type=MessageTypes.INTENTION_TO_STOP, payload=StopPayload(direction=CustomVec2i.up()))
        )

        controls[arcade.key.S] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE, payload=MovePayload(direction=CustomVec2i.down())),
            key_up=MessageBody(message_type=MessageTypes.INTENTION_TO_STOP, payload=StopPayload(direction=CustomVec2i.down()))
        )

        controls[arcade.key.A] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE, payload=MovePayload(direction=CustomVec2i.left())),
            key_up=MessageBody(message_type=MessageTypes.INTENTION_TO_STOP, payload=StopPayload(direction=CustomVec2i.left()))
        )

        controls[arcade.key.D] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE, payload=MovePayload(direction=CustomVec2i.right())),
            key_up=MessageBody(message_type=MessageTypes.INTENTION_TO_STOP, payload=StopPayload(direction=CustomVec2i.right()))
        )

        puppeteer = Puppeteer(puppet=unit, controls=controls)
        puppeteer.add_behaviour(Behaviours.POSSESSOR)
        level.actors_collection.add(puppeteer)
        # End of Puppeteer setup

        # Prison walls
        # for coordinates in [CustomVec2i(1, 0), CustomVec2i(1, 1), CustomVec2i(0, 1)]:

        # for prison in maze(level.grid_width, level.grid_height):
        #   level.actors_collection.add(prison)

        #for coordinates in [CustomVec2i(1, 1), CustomVec2i(0, 1)]:
        #   prison_body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
        #   prison_shape = Shape(get_icon_path(Icons.WALLS))
        #   # Unique name would be created automatically.
        #   level.actors_collection.add(StaticObject(
        #       body=prison_body,
        #       shape=prison_shape,
        #       coordinates=coordinates,
        #       height=100,
        #       weight=100,
        #   ))
        # End of prison walls

        for coordinate_holder in level.actors_collection.get_by_type(CoordinateHolder, CoordinateHolderCollection):
            level.grid.place(coordinate_holder, coordinate_holder.coordinates)


        self.levels = { "level1": level }
