# Image Swipe 3: Local Image Swipe
# Image Swipe 3 implementation for local image sorting.

# Imports
import os

from ..ImageSwipeShared import VALID_IMAGE_EXTS, fullpath
from ..ImageSwipeCore import ImageSwipeCore
from ..TextureModel import TextureModel
# Classes
class SwipeLocal:
    """
    Image Swipe 3 implementation for local image sorting.
    """
    # Constructor
    def __init__(self,
        inputDir: str,
        outputDir: str,
        extensions: list[str] = VALID_IMAGE_EXTS,
        debug: bool = False
    ):
        """
        inputDir: The directory to load images from.
        outputDir: The directory to place output directories in.
        extensions: A list of valid image extensions.
        debug: If `True`, debug features will be enabled.
        """
        # Record info
        self.extensions = extensions
        self.debug = debug

        # Get full paths
        self.inputDir = fullpath(inputDir)
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
        # Load the images from the input directory
        images = self.__loadImagesFromDir()

        # Add the images to the core
        self.core.addImagesToQueue(images)

        # Display the core
        self.core.display(onFirstFrame=self.__onFirstFrame)

    # Private Functions
    def __onFirstFrame(self):
        """
        Triggered by `core` on the first frame after starting the interface.
        """
        # Start the queue
        self.core.startQueue()

    def __loadImagesFromDir(self) -> list[TextureModel]:
        """
        Loads images from the input directory.

        Returns a list of TextureModel objects.
        """
        # Loop through the target directory
        images: list[TextureModel] = []
        for f in os.listdir(self.inputDir):
            # Build the filepath
            filePath = os.path.join(self.inputDir, f)

            # Check if a file
            if os.path.isfile(filePath):
                # Get the file details
                fileName, fileExt = os.path.splitext(f)

                # Check if in the whitelist
                if fileExt.lower() in VALID_IMAGE_EXTS:
                    images.append(TextureModel(filePath, fileName))

        # Debug print
        if self.debug:
            print(f"Added {len(images)} images to the queue from: {self.inputDir}")

        return images

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
