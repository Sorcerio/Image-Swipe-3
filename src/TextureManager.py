# Image Swipe 3: Texture Manager
# Provides functionality for managing textures.

# Imports
import os
from typing import Union, Optional
import dearpygui.dearpygui as dpg

from .ImageSwipeShared import ASSETS_DIR, fullpath

# Classes
class TextureManager:
    """
    Provides functionality for managing textures.
    """
    # Constants
    _PATH_IMAGE_ERROR = fullpath(os.path.join(ASSETS_DIR, "error.png"))

    _TAG_TEXTURE_REGISTRY = "textureRegistry"
    _TAG_IMAGE_ERROR = "errorImage"

    # Constructor
    def __init__(self):
        """
        **Must** be initialized after `setup_dearpygui()` is called.
        """
        # Check if the error image exists
        if not os.path.exists(self._PATH_IMAGE_ERROR):
            # Won't work without this
            raise FileNotFoundError(f"No error image file at: {self._PATH_IMAGE_ERROR}")

        # Register the error image
        self.registerImage(self._PATH_IMAGE_ERROR, self._TAG_IMAGE_ERROR)

    # Functions
    def showTextureRegistry(self):
        """
        Shows the texture registry.
        """
        # Show the texture registry
        dpg.configure_item(self._TAG_TEXTURE_REGISTRY, show=True)

    def registerImage(self, path: str, tag: Union[int, str], label: Optional[str] = None):
        """
        Registers the given image with the texture register as a static texture.

        path: The path to the image. If `path` does not exist, the error image will be used instead for the given `tag`.
        tag: The tag that will be used to reference the image later.
        label: A text label to associate with the image. If not provided, the `tag` will be used.
        """
        # Check if the image exists
        if not os.path.exists(path):
            # Show the error image
            self.registerImage(self._PATH_IMAGE_ERROR, tag)

            # Show an error
            print(f"Image not found at: {path}")

            # Return
            return

        # Load the image
        width, height, channels, data = dpg.load_image(path)

        # Add to the texture registry
        with dpg.texture_registry(label="Texture Registry", tag=self._TAG_TEXTURE_REGISTRY):
            dpg.add_static_texture(width, height, data, tag=tag, label=(label or tag))

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
