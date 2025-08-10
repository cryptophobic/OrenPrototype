import arcade

from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.config import Behaviours, NpcAnimations, animation_paths
from app.core.geometry.shape import Shape
from app.core.physics.body import Body, CollisionMatrix, CollisionResponse
from app.core.vectors import CustomVec2i
from app.engine.grid.grid import Grid
from app.engine.message_broker.types import Controls, KeyBinding, MessageBody, MessageTypes, StopPayload, MovePayload
from app.maps.level import Level, map_dir
from app.objects.coordinate_holder import CoordinateHolder
from app.objects.puppeteer import Puppeteer
from app.objects.static_object import StaticObject
from app.objects.types import UnitStats
from app.objects.unit import Unit
from app.protocols.objects.unit_protocol import UnitProtocol
from app.registry.icon_registry import get_icon_path, Icons


class LevelFactory:
    def __init__(self):
        level = Level()
        self.level_name = "level1"
        level.grid_width = 50
        level.grid_height = 38

        level.current_map = map_dir / "test_level" / "test.tmx"

        level.grid = Grid(width=level.grid_width, height=level.grid_height)

        # Cursor setup
        cursor_body = Body(CollisionMatrix(response=CollisionResponse.OVERLAP))
        cursor_shape = Shape(get_icon_path(Icons.CURSOR))
        cursor_actor = CoordinateHolder(
            body=cursor_body,
            shape=cursor_shape,
            coordinates=CustomVec2i(4, 8),
            name="Cursor")
        cursor_actor.add_behaviour(Behaviours.CURSOR)
        level.actors_collection.add(cursor_actor)
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
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE_DISCRETE, payload=MovePayload(CustomVec2i.up())),
            repeat_delta=150
        )
        controls[arcade.key.DOWN] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE_DISCRETE, payload=MovePayload(CustomVec2i.down())),
            repeat_delta=150
        )
        controls[arcade.key.LEFT] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE_DISCRETE, payload=MovePayload(CustomVec2i.left())),
            repeat_delta=150
        )
        controls[arcade.key.RIGHT] = KeyBinding(
            key_down=MessageBody(message_type=MessageTypes.INTENTION_TO_MOVE_DISCRETE, payload=MovePayload(CustomVec2i.right())),
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

        for coordinate_holder in level.actors_collection.get_by_type(CoordinateHolder, CoordinateHolderCollection):
            level.grid.place(coordinate_holder, coordinate_holder.coordinates)

        self.levels = { self.level_name: level }

    def add_wall(self, place: CustomVec2i):
        prison_body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
        prison_shape = None  # No need to draw, it is drawn by a scene
        prison = StaticObject(
            body=prison_body,
            shape=prison_shape,
            coordinates=place,
            height=100,
            weight=100,
        )
        self.levels[self.level_name].actors_collection.add(prison)
        self.levels[self.level_name].grid.place(prison, prison.coordinates)

