from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, List

import arcade

from app.collections.actor_collection import ActorCollection
from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.collections.static_object_collection import StaticObjectCollection
from app.config import Behaviours, NpcAnimations, animation_paths
from app.core.geometry.shape import Shape
from app.core.physics.body import Body, CollisionMatrix, CollisionResponse
from app.core.vectors import CustomVec2i
from app.config import Y_MODIFIER
from app.engine.game_view.tmx_animation_parser import TMXAnimationParser
from app.engine.grid.grid import Grid
from app.engine.message_broker.types import Controls, KeyBinding, MessageBody, MessageTypes, StopPayload, MovePayload
from app.objects.coordinate_holder import CoordinateHolder
from app.objects.puppeteer import Puppeteer
from app.objects.static_object import StaticObject
from app.objects.types import UnitStats
from app.objects.unit import Unit
from app.protocols.engine.grid.grid_protocol import GridProtocol
from app.protocols.objects.unit_protocol import UnitProtocol
from app.registry.icon_registry import get_icon_path, Icons

map_dir = current_path = Path(__file__).parent / "tiles"


@dataclass
class Level:
    name: str = ""
    coordinate_holders: CoordinateHolderCollection = field(default_factory=CoordinateHolderCollection)
    static_objects: StaticObjectCollection = field(default_factory=StaticObjectCollection)
    actors_collection: ActorCollection = field(default_factory=ActorCollection)
    grid: GridProtocol = None
    grid_width: int = 0
    grid_height: int = 0
    current_map: Optional[Path] = None
    tmx_parser: Optional[TMXAnimationParser] = None  # TMXAnimationParser instance

    def place_all_coordinate_holders(self):
        """Place all coordinate holders on the grid"""
        for coordinate_holder in self.actors_collection.get_by_type(CoordinateHolder, CoordinateHolderCollection):
            self.grid.place(coordinate_holder, coordinate_holder.coordinates)


class LevelBuilder(ABC):
    def __init__(self, name: str, width: int, height: int, map_path: Optional[Path] = None):
        self.level = Level()
        self.level.name = name
        self.level.grid_width = width
        self.level.grid_height = height
        self.level.current_map = map_path
        self.level.grid = Grid(width=width, height=height)

    @abstractmethod
    def create_entities(self):
        """Override this to create level-specific entities"""
        pass

    @abstractmethod
    def setup_controls(self) -> Controls:
        """Override this to setup level-specific controls"""
        pass

    def create_cursor(self, position: CustomVec2i, name: str = "Cursor") -> CoordinateHolder:
        """Create a cursor entity"""
        body = Body(CollisionMatrix(response=CollisionResponse.OVERLAP))
        shape = Shape(get_icon_path(Icons.CURSOR))
        cursor = CoordinateHolder(body=body, shape=shape, coordinates=position, name=name)
        cursor.add_behaviour(Behaviours.CURSOR)
        return cursor

    def create_unit(self, position: CustomVec2i, stats: UnitStats, icon: Icons, 
                    animations: Dict[NpcAnimations, NpcAnimations], name: str,
                    behaviours: list[Behaviours] = None) -> UnitProtocol:
        """Create a unit with animations and behaviours"""
        if behaviours is None:
            behaviours = [Behaviours.DISCRETE_MOVER, Behaviours.BUFFERED_MOVER]
        
        body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
        shape = Shape(get_icon_path(icon))
        
        # Setup animations
        for anim_key, anim_value in animations.items():
            shape.animations.set(animation_paths[anim_value].animation, anim_key)
        
        unit = Unit(body=body, shape=shape, coordinates=position, stats=stats, name=name)
        
        # Add behaviours
        for behaviour in behaviours:
            unit.add_behaviour(behaviour)
        
        return unit

    def create_wall(self, position: CustomVec2i, height: int = 100, weight: int = 100) -> StaticObject:
        """Create a wall static object"""
        body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
        shape = None  # No need to draw, it is drawn by a scene
        wall = StaticObject(body=body, shape=shape, coordinates=position, height=height, weight=weight)
        return wall

    def create_standard_controls(self) -> Controls:
        """Create standard WASD + Arrow key controls"""
        controls = Controls()
        
        # Arrow keys for discrete movement
        controls[arcade.key.UP] = KeyBinding(
            key_down=MessageBody(
                message_type=MessageTypes.INTENTION_TO_MOVE_DISCRETE,
                payload=MovePayload(CustomVec2i.up())),
            repeat_delta=150)

        controls[arcade.key.DOWN] = KeyBinding(
            key_down=MessageBody(
                message_type=MessageTypes.INTENTION_TO_MOVE_DISCRETE,
                payload=MovePayload(CustomVec2i.down())),
            repeat_delta=150)

        controls[arcade.key.LEFT] = KeyBinding(
            key_down=MessageBody(
                message_type=MessageTypes.INTENTION_TO_MOVE_DISCRETE,
                payload=MovePayload(CustomVec2i.left())),
            repeat_delta=150)

        controls[arcade.key.RIGHT] = KeyBinding(
            key_down=MessageBody(
                message_type=MessageTypes.INTENTION_TO_MOVE_DISCRETE,
                payload=MovePayload(CustomVec2i.right())),
            repeat_delta=150)

        # WASD for smooth movement
        controls[arcade.key.W] = KeyBinding(
            key_down=MessageBody(
                message_type=MessageTypes.INTENTION_TO_MOVE,
                payload=MovePayload(direction=CustomVec2i.up())),

            key_up=MessageBody(
                message_type=MessageTypes.INTENTION_TO_STOP,
                payload=StopPayload(direction=CustomVec2i.up())))

        controls[arcade.key.S] = KeyBinding(
            key_down=MessageBody(
                message_type=MessageTypes.INTENTION_TO_MOVE,
                payload=MovePayload(direction=CustomVec2i.down())),

            key_up=MessageBody(
                message_type=MessageTypes.INTENTION_TO_STOP,
                payload=StopPayload(direction=CustomVec2i.down())))

        controls[arcade.key.A] = KeyBinding(
            key_down=MessageBody(
                message_type=MessageTypes.INTENTION_TO_MOVE,
                payload=MovePayload(direction=CustomVec2i.left())),

            key_up=MessageBody(
                message_type=MessageTypes.INTENTION_TO_STOP,
                payload=StopPayload(direction=CustomVec2i.left())))

        controls[arcade.key.D] = KeyBinding(
            key_down=MessageBody(
                message_type=MessageTypes.INTENTION_TO_MOVE,
                payload=MovePayload(direction=CustomVec2i.right())),

            key_up=MessageBody(
                message_type=MessageTypes.INTENTION_TO_STOP,
                payload=StopPayload(direction=CustomVec2i.right())))
        
        return controls

    def create_puppeteer(self, puppet: UnitProtocol, controls: Optional[Controls] = None) -> Puppeteer:
        """Create a puppeteer with controls"""
        if controls is None:
            controls = self.setup_controls()
        
        puppeteer = Puppeteer(puppet=puppet, controls=controls)
        puppeteer.add_behaviour(Behaviours.POSSESSOR)
        return puppeteer

    def get_tmx_parser(self):
        """Get TMX parser, creating it if needed"""
        if self.level.tmx_parser is None and self.level.current_map:
            from app.engine.game_view.tmx_animation_parser import TMXAnimationParser
            self.level.tmx_parser = TMXAnimationParser(str(self.level.current_map))
        return self.level.tmx_parser

    def create_static_objects_from_tmx_layer(self, layer_name: str, 
                                           tile_to_object_map: Optional[Dict[int, str]] = None):
        """Create static objects from TMX layer tiles
        
        Args:
            layer_name: Name of the TMX layer to process
            tile_to_object_map: Optional mapping of tile_id -> object_type
                               If None, all non-zero tiles become walls
        """
        parser = self.get_tmx_parser()
        if not parser or layer_name not in parser.map_layers:
            return

        layer_data = parser.map_layers[layer_name]
        
        for y, row in enumerate(layer_data):
            for x, tile_id in enumerate(row):
                if tile_id != 0:  # Non-empty tile
                    # Apply Y_MODIFIER to handle coordinate system differences
                    if Y_MODIFIER == -1:
                        # Arcade coordinate system: flip Y to match game grid
                        adjusted_y = parser.map_height - 1 - y
                    else:
                        # Pygame coordinate system: use Y as-is
                        adjusted_y = y
                    position = CustomVec2i(x, adjusted_y)
                    
                    if tile_to_object_map and tile_id in tile_to_object_map:
                        object_type = tile_to_object_map[tile_id]
                        static_obj = self._create_static_object_by_type(position, object_type)
                    else:
                        # Default to wall
                        static_obj = self.create_wall(position)
                    
                    self.level.actors_collection.add(static_obj)

    def _create_static_object_by_type(self, position: CustomVec2i, object_type: str) -> StaticObject:
        """Create different types of static objects based on type string"""
        if object_type.lower() == "wall":
            return self.create_wall(position)
        elif object_type.lower() == "water":
            return self.create_water(position)
        elif object_type.lower() == "obstacle":
            return self.create_obstacle(position)
        else:
            # Default to wall for unknown types
            return self.create_wall(position)

    def create_water(self, position: CustomVec2i, height: int = 50, weight: int = 1) -> StaticObject:
        """Create a water static object"""
        body = Body(CollisionMatrix(response=CollisionResponse.OVERLAP))  # Water allows overlap but may slow movement
        shape = None  # No need to draw, it is drawn by the scene
        water = StaticObject(body=body, shape=shape, coordinates=position, height=height, weight=weight)
        return water

    def create_obstacle(self, position: CustomVec2i, height: int = 75, weight: int = 50) -> StaticObject:
        """Create a general obstacle static object"""
        body = Body(CollisionMatrix(response=CollisionResponse.BLOCK))
        shape = None  # No need to draw, it is drawn by the scene
        obstacle = StaticObject(body=body, shape=shape, coordinates=position, height=height, weight=weight)
        return obstacle

    def build(self) -> Level:
        """Build the complete level"""
        self.create_entities()
        self.level.place_all_coordinate_holders()
        return self.level


class LevelLoader:
    """Friendly interface for loading levels"""
    
    def __init__(self):
        self.available_levels: Dict[str, type] = {}
    
    def register_level(self, name: str, builder_class: type):
        """Register a level builder class"""
        self.available_levels[name] = builder_class
    
    def list_levels(self) -> list[str]:
        """Get list of available level names"""
        return list(self.available_levels.keys())
    
    def load_level(self, name: str) -> Level:
        """Load a level by name with friendly error messages"""
        if name not in self.available_levels:
            available = ", ".join(self.available_levels.keys())
            raise ValueError(f"Level '{name}' not found. Available levels: {available}")
        
        try:
            builder_class = self.available_levels[name]
            builder = builder_class()
            level = builder.build()
            print(f"✓ Level '{name}' loaded successfully")
            print(f"  - Grid size: {level.grid_width}x{level.grid_height}")
            print(f"  - Actors: {len(level.actors_collection)}")
            if level.current_map:
                print(f"  - Map file: {level.current_map.name}")
            return level
        except Exception as e:
            print(f"✗ Failed to load level '{name}': {e}")
            raise
