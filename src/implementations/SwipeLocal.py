# Image Swipe 3: Local Image Swipe
# Image Swipe 3 implementation for local image sorting.

# Imports
import os
from typing import Union, Any
import dearpygui.dearpygui as dpg

from ..ImageSwipeShared import VALID_IMAGE_EXTS, fullpath, loadImagesFromDir
from ..ImageSwipeCore import ImageSwipeCore

# Classes
class SwipeLocal:
    """
    Image Swipe 3 implementation for local image sorting.
    """
    # Constants
    SIZE_FILESELECT = (800, 600)

    # Constructor
    def __init__(self,
        outputDir: str,
        rootDir: str = "",
        extensions: list[str] = VALID_IMAGE_EXTS,
        debug: bool = False
    ):
        """
        outputDir: The directory to place output directories in.
        inputDir: The directory to start the directory selector dialog in.
        extensions: A list of valid image extensions.
        debug: If `True`, debug features will be enabled.
        """
        # Record info
        self.extensions = extensions
        self.debug = debug

        # Get full paths
        self.rootDir = fullpath(rootDir)
        self.outputDir = fullpath(outputDir)

        # Prepare the core
        self.core = ImageSwipeCore(
            outputDir,
            debug=debug
        )

    # Functions
    def display(self):
        """
        Displays the local image swipe interface.
        """
        # Display the core
        self.core.display(onFirstFrame=self.__onFirstFrame)

    # Private Functions
    def __onFirstFrame(self):
        """
        Triggered by `core` on the first frame after starting the interface.
        """
        # Show the input directory file selector
        dpg.add_file_dialog(
            label="Select Image Directory",
            width=self.SIZE_FILESELECT[0],
            height=self.SIZE_FILESELECT[1],
            callback=self.__inputDirSelectedCallback,
            cancel_callback=(lambda : dpg.stop_dearpygui()),
            directory_selector=True,
            default_path=self.rootDir
        )

    # Callback Functions
    def __inputDirSelectedCallback(self, sender: Union[int, str], selection: dict[str, Any]):
        """
        Callback for handling when the input directory is selected.

        sender: The tag of the sender.
        selection: The file selection data as returned by the file dialog.
        """
        # Check if the user selected a file
        if "file_path_name" not in selection:
            raise FileNotFoundError("No directory was selected.")

        # Get the full input path
        inputDir = fullpath(selection["file_path_name"])

        # Validate the path
        if not os.path.isdir(inputDir):
            raise FileNotFoundError(f"Invalid directory selected: {inputDir}")

        # Load the images from the input directory
        images = loadImagesFromDir(inputDir, debug=self.debug)

        # Add the images to the core
        self.core.addImagesToQueue(images)

        # Start the queue
        self.core.startQueue()

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
