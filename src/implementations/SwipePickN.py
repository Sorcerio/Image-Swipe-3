# Image Swipe 3: Pick N
# Image Swipe 3 implementation for picking N number of images from a local directory.

# Imports
import os
import argparse
import random

import dearpygui.dearpygui as dpg

from .SwipeLocal import SwipeLocal
from ..ImageSwipeShared import VALID_IMAGE_EXTS, corePaths
from ..ImageSwipeCore import ImageSwipeCore
from ..ActionButtonModel import CustomButtonModel
from ..TextureModel import TextureModel

# Classes
class SwipePickN(SwipeLocal):
    # Constants
    CLI_PROG = "pickn"
    CLI_DESC = "Pick N number of images from a local directory."

    KEEP_DIR = "Keep"

    # Constructor
    def __init__(self,
        outputDir: str,
        rootDir: str = "",
        extensions: list[str] = VALID_IMAGE_EXTS,
        keepCount: int = 1,
        debug: bool = False
    ):
        """
        outputDir: The directory to place output directories in.
        rootDir: The directory to start the directory selector dialog in.
        extensions: A list of valid image extensions.
        keepCount: The number of images to keep.
        debug: If `True`, debug features will be enabled.
        """
        # Ignores super class constructor

        # Record info
        self.extensions = extensions
        self.debug = debug
        self._keepCount = keepCount
        self._keptTags: list[int] = [] # Tags of the kept images

        # Get the paths
        outputDir, self.rootDir = corePaths(outputDir, rootDir)

        # Prepare buttons
        buttons: list[CustomButtonModel] = [
            CustomButtonModel(
                "Keep",
                self.__keepButtonCallback
            ),
            CustomButtonModel(
                "Discard",
                self.__discardButtonCallback
            )
        ]

        # Prepare the core
        self.core = ImageSwipeCore(
            outputDir,
            buttons=buttons,
            hotkeys=None,
            onQueueComplete=self.__queueCompleteCallback,
            toolbarFileMenuHook=self.__fileMenuOptions,
            debug=debug
        )

    # Static Functions
    @classmethod
    def fromArgs(cls, args: argparse.Namespace) -> 'SwipePickN':
        """
        Creates a new instance of this implementation using the given command line arguments.

        args: The command line arguments to use.

        Returns the new instance.
        """
        return cls(
            args.output,
            rootDir=args.root,
            extensions=args.extensions,
            keepCount=args.keep,
            debug=args.debug
        )

    @staticmethod
    def buildParser(parser: argparse.ArgumentParser):
        """
        Sets up the given command line parser with the required arguments for this implementation.

        parser: The parser to setup.
        """
        # Add required arguments
        parser.add_argument("output", type=str, help="The directory to place output directories in.")

        # Add optional arguments
        parser.add_argument("-r", "--root", help="The directory to start the directory selector dialog in.", type=str, default="")
        parser.add_argument("-e", "--extensions", help=f"A list of valid image extensions. (Default: {', '.join(VALID_IMAGE_EXTS)})", metavar="EXT", nargs='+', default=VALID_IMAGE_EXTS)
        parser.add_argument("-k", "--keep", help="The number of images to keep. (Default: 1)", metavar="NUM", type=int, default=1)
        parser.add_argument("--debug", help="If provided, enables debug mode.", action="store_true")

    # Callback Functions
    def __keepButtonCallback(self, btnData: str):
        """
        Callback to handle "Keep" button presses.

        btnData: None.
        """
        # Get the current image
        _, imgTex = tuple(self.core.getPresentedImages().items())[0]

        # Record the image to keep
        self._keptTags.append(imgTex.tag)

        # Report
        if self.debug:
            print(f"Kept image Tag {imgTex.tag}: {self._keptTags}")

        # Advance to the next image
        self.core.showNextImage()

    def __discardButtonCallback(self, btnData):
        """
        Callback to handle "Discard" button presses.

        btnData: None.
        """
        # Report
        if self.debug:
            _, imgTex = tuple(self.core.getPresentedImages().items())[0]
            print(f"Discarded image Tag {imgTex.tag}: {self._keptTags}")

        # Advance to the next image
        self.core.showNextImage()

    def __queueCompleteCallback(self):
        """
        Callback to handle the queue being completed.
        """
        # Report
        if self.debug:
            print(f"Queue round completed retaining: {self._keptTags}")

        # Check the number of kept images
        if len(self._keptTags) <= self._keepCount:
            # All rounds complete
            self.__finalizeSelection()
        else:
            # Go for another round
            # Remove the unkept images from queue
            keptImages: list[TextureModel] = []
            for imgTex in self.core._images:
                # Check if kept
                if imgTex.tag in self._keptTags:
                    # Report
                    if self.debug:
                        print(f"Keeping image Tag {imgTex.tag} in queue: {imgTex}")

                    # Keep it in the queue
                    keptImages.append(imgTex)

            # Shuffle the kept images
            random.shuffle(keptImages)

            # Reset the kept tags tracker
            self._keptTags = []

            # Set the core queue
            self.core.setImageQueue(keptImages)

            # Start queue again
            self.core.startQueue()

    def __finalizeSelection(self):
        """
        Saves the current queue to disk and ends the program.
        """
        # Save the kept images
        for i, imgTex in enumerate(self.core._images):
            # Check if kept
            if imgTex.tag in self._keptTags:
                # Report
                if self.debug:
                    print(f"Saving image Tag {imgTex.tag}")

                # Save the image
                self.core.saveImageAtIndex(
                    i,
                    os.path.join(
                        self.core.outputDir,
                        self.KEEP_DIR,
                        os.path.basename(imgTex.filepath)
                    )
                )

        # Report
        if self.debug:
            print(f"Saved {len(self._keptTags)} of {self._keepCount} images.")

        # Show queue complete alert
        self.core.createQueueCompleteAlert()

    def __keepRestOfQueue(self):
        """
        Keeps all the images from the current image to the end of the queue as well as any in the current keep list.
        """
        # Record the current image and all subsequent
        for imgTex in self.core._images[self.core._curImageIndex:]:
            self._keptTags.append(imgTex.tag)

        # Remove duplicates
        self._keptTags = list(set(self._keptTags))

        # Report
        if self.debug:
            print(f"Keeping items in queue: {self._keptTags}")

        # Finalize
        self.__finalizeSelection()

    def __fileMenuOptions(self):
        asIs = dpg.add_menu_item(label="Accept As Is", callback=self.__keepRestOfQueue)
        with dpg.tooltip(asIs):
            dpg.add_text("Accept all images currently in the queue regardless of the keep count.")

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
