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

        # Prepare records
        self._textures: list[Union[int, str]] = []
        self._sizes: dict[Union[int, str], tuple[int, int]] = {}

        # Register the error image
        self.registerTexture(self._PATH_IMAGE_ERROR, self._TAG_IMAGE_ERROR)

    # Functions
    def showTextureRegistry(self):
        """
        Shows the texture registry.
        """
        # Show the texture registry
        dpg.configure_item(self._TAG_TEXTURE_REGISTRY, show=True)

    def registerTexture(self, path: str, tag: Union[int, str], label: Optional[str] = None):
        """
        Registers the given image with the texture register as a static texture.

        path: The path to the image. If `path` does not exist, the error image will be used instead for the given `tag`.
        tag: The tag that will be used to reference the image later.
        label: A text label to associate with the image. If not provided, the `tag` will be used.
        """
        # Check if the image exists
        if not os.path.exists(path):
            # Show the error image
            self.registerTexture(self._PATH_IMAGE_ERROR, tag)

            # Show an error
            print(f"Image not found at: {path}")

            # Return
            return

        # Load the image
        width, height, channels, data = dpg.load_image(path)

        # Add to the texture registry
        if not dpg.does_item_exist(self._TAG_TEXTURE_REGISTRY):
            # First time
            with dpg.texture_registry(label="Texture Registry", tag=self._TAG_TEXTURE_REGISTRY):
                dpg.add_static_texture(width, height, data, tag=tag, label=(label or tag))
        else:
            # Subsequent times
            dpg.add_static_texture(width, height, data, tag=tag, label=(label or tag), parent=self._TAG_TEXTURE_REGISTRY)

        # Record texture info
        self._textures.append(tag)
        self._sizes[tag] = (width, height)

    # TODO: removeTexture

    # Static Functions
    @staticmethod
    def calcBestFitSize(contentSize: tuple, containerSize: tuple, shouldFit: bool) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Calculates the best fit size and center anchor point for the `contentSize` within the `containerSize`.

        contentSize: The size of the content like `(width, height)`.
        containerSize: The size of the container like `(width, height)`.
        shouldFit: If `True`, the image will fit inside the container. If `False`, the image will stretch to fill the container.

        Returns the best fit size of the content as a tuple like `(width, height)` and the origin offset as a tuple like `(x, y)`.
        """
        # Calculate resize ratio
        if shouldFit:
            # Fit inside the canvas
            resizeRatio = min(containerSize[0] / contentSize[0], containerSize[1] / contentSize[1])
        else:
            # Stretch across canvas
            resizeRatio = max(containerSize[0] / contentSize[0], containerSize[1] / contentSize[1])

        # Calculate the best size for the content
        finalW = round(contentSize[0] * resizeRatio)
        finalH = round(contentSize[1] * resizeRatio)

        # Calculate paste offset
        pasteOffsetX = 0
        pasteOffsetY = 0

        if finalW > containerSize[0]:
            # Need to adjust X
            pasteOffsetX = -(round((finalW - containerSize[0]) / 2))

        if finalH > containerSize[1]:
            # Need to adjust Y
            pasteOffsetY = -(round((finalH - containerSize[1]) / 2))

        return (
            (finalW, finalH),
            (pasteOffsetX, pasteOffsetY)
        )

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
