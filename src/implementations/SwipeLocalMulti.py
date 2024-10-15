# Image Swipe 3: Local Multiple Image Swipe
# Image Swipe 3 implementation for local image sorting with multiple images per swipe.

# Imports
import os
import argparse

from .SwipeLocal import SwipeLocal
from ..ImageSwipeShared import VALID_IMAGE_EXTS, corePaths
from ..ImageSwipeCore import ImageSwipeCore
from ..ActionButtonModel import ActionButtonModel, RejectButtonModel

# Classes
class SwipeLocalMulti(SwipeLocal):
    """
    Image Swipe 3 implementation for local image sorting where multiple images are shown but only one can be selected.
    """
    # Constants
    CLI_PROG = "localmulti"
    CLI_DESC = "Sort images from a local directory with multiple images per swipe."

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
        imagesPer: The number of images to show at once.
        extensions: A list of valid image extensions.
        debug: If `True`, debug features will be enabled.
        """
        # Ignores super class constructor

        # Record info
        self.extensions = extensions
        self.debug = debug

        # Get the paths
        outputDir, self.rootDir = corePaths(outputDir, rootDir)

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
            outputDir,
            buttons=buttons,
            hotkeys=None,
            preloadBuffer=round(3 * imagesPer),
            imgPerDisplay=imagesPer,
            iterPerAction=imagesPer,
            debug=debug
        )

    # Static Functions
    @classmethod
    def fromArgs(cls, args: argparse.Namespace) -> 'SwipeLocalMulti':
        """
        Creates a new instance of this implementation using the given command line arguments.

        args: The command line arguments to use.

        Returns the new instance.
        """
        return cls(
            args.output,
            rootDir=args.root,
            imagesPer=args.imagesPer,
            extensions=args.extensions,
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
        parser.add_argument("-i", "--imagesPer", help="The number of images to show at once. (Default: %(default)s)", metavar="NUM", type=int, default=2)
        parser.add_argument("-e", "--extensions", help=f"A list of valid image extensions. (Default: {', '.join(VALID_IMAGE_EXTS)})", metavar="EXT", nargs='+', default=VALID_IMAGE_EXTS)
        parser.add_argument("--debug", help="If provided, enables debug mode.", action="store_true")

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

        # Save the current image
        self.core.saveImageAtIndex(
            curIndex,
            os.path.join(
                self.core.outputDir,
                dirName,
                os.path.basename(curImg.filepath)
            )
        )

        # Show the next image
        self.core.showNextImage()

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
