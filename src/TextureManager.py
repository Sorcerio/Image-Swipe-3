# Image Swipe 3: Texture Manager
# Provides functionality for managing textures.

# Imports
import os
from typing import Union, Optional

import dearpygui.dearpygui as dpg
import numpy as np
from PIL import Image

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

    MAX_TEXTURE_SIZE = (1080, 1080)

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
        self._textures: list[Union[int, str]] = [] # List of all texture tags
        self._sizes: dict[Union[int, str], tuple[int, int]] = {} # Texture Tag: Image Size

        # Register the error image
        self.registerTexture(self._PATH_IMAGE_ERROR, self._TAG_IMAGE_ERROR)

    # Functions
    def showTextureRegistry(self):
        """
        Shows the texture registry.
        """
        # Make sure it exists
        if not dpg.does_item_exist(self._TAG_TEXTURE_REGISTRY):
            # Create it
            dpg.add_texture_registry(label="Texture Registry", tag=self._TAG_TEXTURE_REGISTRY)

        # Show the texture registry
        dpg.configure_item(self._TAG_TEXTURE_REGISTRY, show=True)

    def registerTexture(self,
        path: str,
        tag: Union[int, str],
        label: Optional[str] = None,
        maxRez: Optional[tuple[int, int]] = MAX_TEXTURE_SIZE
    ):
        """
        Registers the given image with the texture register as a static texture.

        path: The path to the image. If `path` does not exist, the error image will be used instead for the given `tag`.
        tag: The tag that will be used to reference the image later.
        label: A text label to associate with the image. If not provided, the `tag` will be used.
        maxRez: The maximum resolution the image can be like `(width, height)`. If `None` is provided, the image will be loaded at its original resolution.
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
        if maxRez is not None:
            # Load with max size
            width, height, channels, data = self._loadImageWithMaxSize(path, maxRez)
        else:
            # Load normally
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

    def removeTexture(self, tag: Union[int, str]):
        """
        Removes the texture from the texture registry.

        tag: The tag of the texture to remove.
        """
        # Make sure it exists
        if dpg.does_item_exist(tag):
            # Remove it
            dpg.delete_item(tag)

            # Remove from records
            self._textures.remove(tag)
            self._sizes.pop(tag)

    def dumpTextures(self):
        """
        Dumps all textures from the texture registry by deleting the registry.
        """
        # Make sure it exists
        if dpg.does_item_exist(self._TAG_TEXTURE_REGISTRY):
            # Rip
            dpg.delete_item(self._TAG_TEXTURE_REGISTRY)

    # Private Functions
    def _loadImageWithMaxSize(self, path: str, maxSize: tuple[int, int]) -> tuple[int, int, int, bytes]:
        """
        Loads an image for use in DearPyGui constrained within the given `maxSize`.

        path: A path to the image file.
        maxSize: The maximum size the image can be like `(width, height)`.

        Returns the width, height, channels, and data of the image in a format suitable for use with DearPyGui.
        """
        # Load the image
        with Image.open(path).convert("RGBA") as pilImage:
            # Calculate the best fit size
            bestFitSize, _ = self.calcBestFitSize(pilImage.size, maxSize, True)

            # Resize the image
            with pilImage.resize(bestFitSize, Image.Resampling.LANCZOS) as resizedImage:
                newSize = resizedImage.size
                return (
                    newSize[0],
                    newSize[1],
                    4, # RGBA
                    (np.array(resizedImage).flatten() / 255.0) # Flatten and normalize the image
                )

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
