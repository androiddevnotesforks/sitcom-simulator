from .integrations import stability, pillow
from tqdm import tqdm
from typing import List, Optional, Callable, Literal
from sitcom_simulator.models import Script
import os
import atexit

Engine = Literal["stability", "pillow"]

def generate_images(
        script: Script,
        width=768,
        height=1344,
        on_image_generated: Optional[Callable[[int, str], None]] = None,
        engine:Engine="stability",
    ):
    """
    Generates and returns a list of image paths for the given script
    @param script: The script to generate images for
    @param width: The width of the images to generate
    @param height: The height of the images to generate
    @param on_image_generated: A callback to call after each image is generated
    @param engine: The engine to use for generating images
    """
    image_paths: List[str | None] = []
    image_prompts = [clip.image_prompt for clip in script.clips]
    for i, image_prompt in tqdm(enumerate(image_prompts), desc="Generating images", total=len(image_prompts)):
        if not image_prompt:
            image_paths.append(None)
            continue
        if engine == "stability":
            full_prompt = image_prompt + ', ' + script.metadata.art_style
            image_path = stability.generate_image(prompt=full_prompt, width=width, height=height)
        else: # debug engine
            image_path = pillow.generate_image(width, height)
        atexit.register(os.remove, image_path)
        image_paths.append(image_path)
        if on_image_generated:
            on_image_generated(i, image_path)

    return image_paths

def add_images(
        script: Script,
        width=768,
        height=1344,
        on_image_generated: Optional[Callable[[int, str], None]] = None,
        engine:Engine="stability",
    ) -> Script:
    image_paths = generate_images(
        script=script,
        width=width,
        height=height,
        on_image_generated=on_image_generated,
        engine=engine)
    return script.replace(clips=[clip.replace(image_path=image_path) for clip, image_path in zip(script.clips, image_paths)])