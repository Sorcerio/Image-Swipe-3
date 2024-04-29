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

        # Prepare buttons
        buttons: list[ActionButtonModel] = []

        for i in range(imagesPer):
            buttons.append(ActionButtonModel(
                label=f"Keep #{i + 1}",
                action=ActionButtonModel.ACTION_CUSTOM,
                callback=self.__keepButtonCallback,
                userData=(i, "Keep")
            ))

        buttons.append(RejectButtonModel(label="Discard All"))

        # Prepare the core
        self.core = ImageSwipeCore(
            fullpath(outputDir),
            buttons=buttons,
            hotkeys=None,
            preloadBuffer=round(3 * imagesPer),
            imgPerDisplay=imagesPer,
            iterPerAction=imagesPer,
            debug=debug
        )

    # Callback Functions
    def __keepButtonCallback(self, btnData: tuple[int, str]):
        """
        Callback to handle custom "Keep" button presses.

        btnData: A tuple containing the index of the button pressed and the name of the output directory.
        """
        # Extract button data
        btnIndex, dirName = btnData

        # Get the current image
        curIndex, curImg = tuple(self.core.getPresentedImages().items())[btnIndex]

        # Save the selected image
        self.core.saveCurrentImage(os.path.join(
            self.core.outputDir,
            dirName,
            os.path.basename(curImg.filepath)
        ))

        # Show the next image
        self.core.showNextImage()

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
