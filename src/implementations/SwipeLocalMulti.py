# Image Swipe 3: Local Multiple Image Swipe
# Image Swipe 3 implementation for local image sorting with multiple images per swipe.

# Imports
import os
from typing import Union, Any
import dearpygui.dearpygui as dpg

from .SwipeLocal import SwipeLocal
from ..ImageSwipeShared import VALID_IMAGE_EXTS, fullpath, loadImagesFromDir
from ..ImageSwipeCore import ImageSwipeCore
from ..ActionButtonModel import ActionButtonModel, RejectButtonModel

# Classes
class SwipeLocalMulti(SwipeLocal):
    """
    Image Swipe 3 implementation for local image sorting where multiple images are shown but only one can be selected.
    """
    # Constructor
    def __init__(self,
        outputDir: str,
        rootDir: str = "",
        imagesPer: int = 1,
        extensions: list[str] = VALID_IMAGE_EXTS,
        debug: bool = False
    ):
        """
        outputDir: The directory to place output directories in.
        rootDir: The directory to start the directory selector dialog in.
        extensions: A list of valid image extensions.
        debug: If `True`, debug features will be enabled.
        """
        # Ignores super class constructor

        # Record info
        self.extensions = extensions
        self.debug = debug

        # Get full paths
        self.rootDir = fullpath(rootDir)
        self.outputDir = fullpath(outputDir)

        # Prepare buttons
        buttons: list[ActionButtonModel] = []

        for i in range(imagesPer):
            buttons.append(ActionButtonModel(
                label=f"Keep #{i + 1}",
                action=ActionButtonModel.ACTION_CUSTOM,
                callback=self.__keepButtonCallback
            ))

        buttons.append(RejectButtonModel(label="Discard All"))

        # Prepare the core
        self.core = ImageSwipeCore(
            outputDir,
            buttons=buttons,
            hotkeys=None,
            preloadBuffer=round(3 * imagesPer),
            imgPerDisplay=imagesPer,
            iterPerAction=imagesPer,
            debug=debug
        )

    # Callback Functions
    def __keepButtonCallback(self):
        """
        Callback to handle custom "Keep" button presses.
        """
        print("Keep button pressed.")

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
