# Image Swipe 3: Reddit Swipe
# Image Swipe 3 implementation for Reddit browsing.

# Imports
import os
import argparse
from typing import Union, Any
import dearpygui.dearpygui as dpg

from .SwiperImplementation import SwiperImplementation
from ..ImageSwipeShared import VALID_IMAGE_EXTS, fullpath, loadImagesFromDir
from ..ImageSwipeCore import ImageSwipeCore

# Classes
class SwipeReddit(SwiperImplementation):
    """
    Image Swipe 3 implementation for Reddit browsing.
    """
    # Constants
    CLI_PROG = "reddit"
    CLI_DESC = "Browse images from a subreddit."

    SIZE_FILESELECT = (800, 600)

    # Constructor
    def __init__(self,
        outputDir: str,
        debug: bool = False
    ):
        """
        outputDir: The directory to place output directories in.
        debug: If `True`, debug features will be enabled.
        """
        # Record info
        self.debug = debug

        # Prepare the core
        self.core = ImageSwipeCore(
            fullpath(outputDir),
            debug=debug
        )

    # Functions
    def display(self):
        """
        Displays the local image swipe interface.
        """
        # Display the core
        self.core.display(onFirstFrame=self.__onFirstFrame)

    # Static Functions
    @classmethod
    def fromArgs(cls, args: argparse.Namespace) -> 'SwipeReddit':
        """
        Creates a new instance of this implementation using the given command line arguments.

        args: The command line arguments to use.

        Returns the new instance.
        """
        return cls(
            args.output,
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
        parser.add_argument("--debug", help="If provided, enables debug mode.", action="store_true")

    # Private Functions
    def __onFirstFrame(self):
        """
        Triggered by `core` on the first frame after starting the interface.
        """
        # TODO: Allow for sub-reddit selection

    # Callback Functions

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
