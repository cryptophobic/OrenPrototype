import arcade
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SCREEN_TITLE = "TMX Example"


class AnimatedTile(arcade.Sprite):
    def __init__(self, textures, frame_durations):
        super().__init__(textures[0])
        self.textures = textures
        self.frame_durations = frame_durations
        self.current_frame = 0
        self.time_accum = 0

    def update_animation(self, delta_time: float = 1/60,  *args, **kwargs):
        self.time_accum += delta_time * 1000  # convert to ms
        if self.time_accum > self.frame_durations[self.current_frame]:
            self.time_accum = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures)
            self.texture = self.textures[self.current_frame]


class TMXAnimationParser:
    """Parses TMX files to extract tile animation data"""
    
    def __init__(self, tmx_file_path: str):
        self.tmx_path = Path(tmx_file_path)
        self.animations: Dict[int, List[Tuple[int, int]]] = {}  # tile_id -> [(frame_tileid, duration), ...]
        self.tilesets: Dict[str, Dict] = {}  # tileset_name -> tileset_info
        self._parse_tmx()
    
    def _parse_tmx(self):
        """Parse the TMX file to extract animation and tileset information"""
        tree = ET.parse(self.tmx_path)
        root = tree.getroot()
        
        # Parse tilesets
        for tileset in root.findall('tileset'):
            firstgid = int(tileset.get('firstgid'))
            
            # Check if this is an external tileset reference (TSX file)
            if tileset.get('source'):
                print(f"Found external tileset reference: {tileset.get('source')} (firstgid: {firstgid})")
                # For now, skip external tilesets - we'd need to parse the TSX file separately
                continue
            
            # Handle inline tileset
            tileset_info = {
                'firstgid': firstgid,
                'name': tileset.get('name'),
                'tilewidth': int(tileset.get('tilewidth')),
                'tileheight': int(tileset.get('tileheight')),
                'tilecount': int(tileset.get('tilecount')),
                'columns': int(tileset.get('columns'))
            }
            
            # Get image source
            image_elem = tileset.find('image')
            if image_elem is not None:
                tileset_info['image_source'] = image_elem.get('source')
                tileset_info['image_width'] = int(image_elem.get('width'))
                tileset_info['image_height'] = int(image_elem.get('height'))
            
            self.tilesets[tileset_info['name']] = tileset_info
            
            # Parse animations within this tileset
            for tile in tileset.findall('tile'):
                tile_id = int(tile.get('id'))
                global_tile_id = tile_id + tileset_info['firstgid']
                
                animation_elem = tile.find('animation')
                if animation_elem is not None:
                    frames = []
                    for frame in animation_elem.findall('frame'):
                        frame_tileid = int(frame.get('tileid'))
                        duration = int(frame.get('duration'))
                        global_frame_id = frame_tileid + tileset_info['firstgid']
                        frames.append((global_frame_id, duration))
                    
                    self.animations[global_tile_id] = frames
                    print(f"Found animation for tile {global_tile_id}: {len(frames)} frames")
    
    def get_animations(self) -> Dict[int, List[Tuple[int, int]]]:
        """Get all parsed animations"""
        return self.animations
    
    def get_tilesets(self) -> Dict[str, Dict]:
        """Get all parsed tilesets"""
        return self.tilesets
    
    def load_tileset_textures(self) -> Dict[int, arcade.Texture]:
        """Load all textures from tilesets and return a mapping of tile_id -> texture"""
        textures = {}
        
        for tileset_name, tileset_info in self.tilesets.items():
            if 'image_source' not in tileset_info:
                continue
                
            # Build path to tileset image (relative to TMX file)
            image_path = self.tmx_path.parent / tileset_info['image_source']
            
            if not image_path.exists():
                print(f"Warning: Tileset image not found: {image_path}")
                continue
                
            print(f"Loading tileset '{tileset_name}' from {image_path}")
            
            # Load the tileset image
            tileset_texture = arcade.load_texture(str(image_path))
            
            # Extract individual tile textures
            tile_width = tileset_info['tilewidth']
            tile_height = tileset_info['tileheight']
            columns = tileset_info['columns']
            tile_count = tileset_info['tilecount']
            firstgid = tileset_info['firstgid']
            
            for tile_index in range(tile_count):
                # Calculate tile position in the tileset
                col = tile_index % columns
                row = tile_index // columns
                x = col * tile_width
                y = row * tile_height
                
                # Extract tile texture
                global_tile_id = tile_index + firstgid
                try:
                    tile_texture = tileset_texture.crop(x, y, tile_width, tile_height)
                    textures[global_tile_id] = tile_texture
                except Exception as e:
                    print(f"Error loading tile {global_tile_id}: {e}")
            
            print(f"  Loaded {tile_count} tiles from {tileset_name}")
        
        return textures
    
    def create_animated_sprites(self, scaling: float = 1.0) -> Dict[int, AnimatedTile]:
        """Create AnimatedTile sprites for all animations"""
        textures = self.load_tileset_textures()
        animated_sprites = {}
        
        for tile_id, frames in self.animations.items():
            # Get textures for animation frames
            frame_textures = []
            frame_durations = []
            
            for frame_tile_id, duration in frames:
                if frame_tile_id in textures:
                    texture = textures[frame_tile_id]
                    # Note: We'll handle scaling at the sprite level instead of texture level
                    # since arcade doesn't have easy texture scaling methods
                    frame_textures.append(texture)
                    frame_durations.append(duration)
                else:
                    print(f"Warning: Frame texture {frame_tile_id} not found for animation {tile_id}")
            
            if frame_textures:
                animated_sprite = AnimatedTile(frame_textures, frame_durations)
                # Apply scaling to the sprite
                if scaling != 1.0:
                    animated_sprite.scale = scaling
                animated_sprites[tile_id] = animated_sprite
                print(f"Created animated sprite for tile {tile_id} with {len(frame_textures)} frames")
        
        return animated_sprites
    
    def print_animation_info(self):
        """Print information about found animations"""
        print(f"\n=== TMX Animation Info ===")
        print(f"File: {self.tmx_path}")
        print(f"Found {len(self.animations)} animated tiles")
        print(f"Found {len(self.tilesets)} tilesets")
        
        for tileset_name, info in self.tilesets.items():
            print(f"\nTileset '{tileset_name}':")
            print(f"  - First GID: {info['firstgid']}")
            print(f"  - Tile size: {info['tilewidth']}x{info['tileheight']}")
            print(f"  - Tile count: {info['tilecount']}")
            if 'image_source' in info:
                print(f"  - Image: {info['image_source']}")
        
        print(f"\nAnimations:")
        for tile_id, frames in self.animations.items():
            print(f"  Tile {tile_id}: {len(frames)} frames")
            for i, (frame_id, duration) in enumerate(frames):
                print(f"    Frame {i}: tile {frame_id}, duration {duration}ms")


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        map_name = 'c:/Users/dmitr/PycharmProjects/OrenPrototype/app/resources/animations/tiles/Tiled_files/Glades.tmx'
        scaling = 1.4

        # Parse TMX animations first
        print("Parsing TMX animations...")
        self.animation_parser = TMXAnimationParser(map_name)
        self.animation_parser.print_animation_info()

        # Create animated sprites from the parser
        print("\nCreating animated sprites...")
        self.animated_sprites = self.animation_parser.create_animated_sprites(scaling)

        # Optional: choose which layers should use spatial hash for collisions
        layer_options = {
            "Walls": {"use_spatial_hash": True},
        }

        # Load the TMX map
        self.tile_map = arcade.load_tilemap(map_name, scaling, layer_options)

        # Create a Scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Add animated sprites to a new layer
        if self.animated_sprites:
            self.scene.add_sprite_list("Animations")
            for animated_sprite in self.animated_sprites.values():
                # Position the animated sprite (for now, just place them at origin)
                # Later we'd need to match them to actual map tile positions
                animated_sprite.center_x = 100
                animated_sprite.center_y = 100
                self.scene["Animations"].append(animated_sprite)

        # Camera for scrolling/zoom
        self.camera = arcade.Camera2D()

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

    def on_update(self, delta_time: float):
        # Update all animated sprites
        if hasattr(self, 'animated_sprites'):
            for animated_sprite in self.animated_sprites.values():
                animated_sprite.update_animation(delta_time)

def tmx_loader():
    game = MyGame()
    arcade.run()
