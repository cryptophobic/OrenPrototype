from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image
from arcade import Texture

from app.config import NpcAnimations, animation_paths


@dataclass
class LoadedAnimation:
    front: list[Texture]
    back: list[Texture] = field(default_factory=list)
    left: list[Texture] = field(default_factory=list)
    right: list[Texture] = field(default_factory=list)

animation_dir = current_path = Path(__file__).parent.parent / "resources" / "animations"

class AnimationRegistry:

    def __init__(self):
        self.registry: dict[NpcAnimations, LoadedAnimation] = {}

    def slice_animation_strip(self, image_path: Path, start_x: int, start_y: int, frame_width: int, frame_height: int, count: int) -> list[Texture]:
        pil_image = Image.open(image_path)
        frames = []
        for i in range(count):
            box = (
                start_x + i * frame_width,
                start_y,
                start_x + (i + 1) * frame_width,
                start_y + frame_height
            )
            cropped = pil_image.crop(box).convert("RGBA")
            tex = Texture(name=f"frame_{i}", image=cropped)
            frames.append(tex)
        return frames

    def load(self, animation: NpcAnimations):
        animation_path_details = animation_paths[animation]
        sprites_path = animation_dir / animation_path_details.path

        try:
            directions = {
                "front": animation_path_details.front_offset,
                "left": animation_path_details.left_offset,
                "right": animation_path_details.right_offset,
                "back": animation_path_details.back_offset,
            }

            loaded_animation = LoadedAnimation(
                **{
                    direction: self.slice_animation_strip(
                        sprites_path,
                        0,
                        animation_path_details.sprite_height * offset,
                        animation_path_details.sprite_width,
                        animation_path_details.sprite_height,
                        animation_path_details.frames,
                    )
                    for direction, offset in directions.items()
                }
            )

            self.registry[animation] = loaded_animation
        except Exception as e:
            raise ImportError(f"Failed to load behaviour {animation}: {e}") from e

    def get(self, animation: NpcAnimations) -> LoadedAnimation:
        if animation not in self.registry:
            self.load(animation)

        return self.registry.get(animation)

_registry_instance: AnimationRegistry | None = None

def get_animation_registry() -> AnimationRegistry:
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = AnimationRegistry()
    return _registry_instance

