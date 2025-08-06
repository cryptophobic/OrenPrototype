import arcade
from typing import Dict

from app.engine.game_view.animated_sprite import AnimatedSprite
from app.engine.game_view.tmx_animation_parser import TMXAnimationParser

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SCREEN_TITLE = "TMX Example"


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        map_name = 'c:/Users/dmitr/PycharmProjects/OrenPrototype/app/resources/animations/tiles/Tiled_files/Glades.tmx'
        scaling = 1.4

        # Optional: choose which layers should use spatial hash for collisions
        layer_options = {
            "Walls": {"use_spatial_hash": True},
        }

        # Load animated tilemap using factory
        self.scene, self.animated_layers, self.animation_parser = load_animated_tilemap(
            map_name, scaling, layer_options
        )

        # Camera for scrolling/zoom
        self.camera = arcade.Camera2D()

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

    def on_update(self, delta_time: float):
        self.scene.update(delta_time=delta_time)

def load_animated_tilemap(tmx_file_path: str, scaling: float = 1.0, layer_options: Dict = None):
    """
    Factory function to load a TMX tilemap with animated tiles.
    
    Args:
        tmx_file_path: Path to the TMX file
        scaling: Scale factor for sprites
        layer_options: Optional layer configuration for arcade.load_tilemap
    
    Returns:
        tuple: (arcade.Scene, set of animated layer names, TMXAnimationParser)
    """
    print(f"Loading animated tilemap: {tmx_file_path}")
    
    # Parse TMX animations
    animation_parser = TMXAnimationParser(tmx_file_path)
    animation_parser.print_animation_info()
    
    # Create animated sprites
    animated_sprites = animation_parser.create_animated_sprites(scaling)
    
    # Load the base tilemap
    tile_map = arcade.load_tilemap(tmx_file_path, scaling, layer_options or {})
    
    # Create a scene from tilemap
    scene = arcade.Scene.from_tilemap(tile_map)
    
    # Track layers that will contain animated sprites
    animated_layers = set()
    
    # Replace static tiles with animated sprites in their original layers
    if animated_sprites:
        # Get positions of animated tiles grouped by layer
        animated_positions_by_layer = animation_parser.find_animated_tile_positions_by_layer()
        
        # Process each layer that contains animated tiles
        for layer_name, positions in animated_positions_by_layer.items():
            print(f"Processing {len(positions)} animated tiles in layer '{layer_name}'")
            
            # Track this layer as containing animations
            animated_layers.add(layer_name)
            
            # Get the corresponding sprite list from the scene
            if layer_name in scene:
                layer_sprites = scene[layer_name]
                
                # Create positioned animated sprites for this layer
                for tile_id, map_x, map_y in positions:
                    if tile_id in animated_sprites:
                        # Create a new instance of the animated sprite
                        animated_sprite = animated_sprites[tile_id]
                        new_sprite = AnimatedSprite(animated_sprite.textures, animated_sprite.frame_durations)
                        if scaling != 1.0:
                            new_sprite.scale = scaling
                        
                        # Position the sprite using map coordinates
                        world_x = (map_x * tile_map.tile_width * scaling) + (tile_map.tile_width * scaling / 2)
                        world_y = ((animation_parser.map_height - 1 - map_y) * tile_map.tile_height * scaling) + (tile_map.tile_height * scaling / 2)
                        
                        new_sprite.center_x = world_x
                        new_sprite.center_y = world_y
                        
                        # Remove any existing static tile at this position
                        _remove_static_tile_at_position(layer_sprites, world_x, world_y, scaling)
                        
                        # Add the animated sprite to the layer
                        layer_sprites.append(new_sprite)
                        print(f"Replaced static tile with animated tile {tile_id} at ({map_x}, {map_y}) in layer '{layer_name}'")
    
    return scene, animated_layers, animation_parser


def _remove_static_tile_at_position(sprite_list: arcade.SpriteList, world_x: float, world_y: float, tolerance: float = 1.0):
    """Remove any static tile sprite at the specified world coordinates"""
    # Find sprites that are close to the target position
    to_remove = []
    for sprite in sprite_list:
        if (abs(sprite.center_x - world_x) < tolerance and 
            abs(sprite.center_y - world_y) < tolerance and
            not isinstance(sprite, AnimatedSprite)):  # Don't remove animated tiles
            to_remove.append(sprite)
    
    # Remove the found sprites
    for sprite in to_remove:
        sprite.remove_from_sprite_lists()
        print(f"Removed static tile at ({world_x:.1f}, {world_y:.1f})")


def tmx_loader():
    game = MyGame()
    arcade.run()
