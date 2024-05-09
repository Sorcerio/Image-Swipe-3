# Image Swipe 3: Reddit Swipe
# Image Swipe 3 implementation for Reddit browsing.

# Imports
import os
import argparse
from enum import Enum
from typing import Union, Any
import dearpygui.dearpygui as dpg

from .SwiperImplementation import SwiperImplementation
from ..ImageSwipeShared import fullpath, createModal
from ..ImageSwipeCore import ImageSwipeCore

# Enums
class PostSource(Enum):
    """
    The post source for Reddit post requests.
    """
    HOT = "hot"
    NEW = "new"
    TOP = "top"

class PostTime(Enum):
    """
    The post time for Reddit post requests.
    """
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    ALL = "all"

# Classes
class SwipeReddit(SwiperImplementation):
    """
    Image Swipe 3 implementation for Reddit browsing.
    """
    # Constants
    CLI_PROG = "reddit"
    CLI_DESC = "Browse images from a subreddit."

    SIZE_SETUP = (404, 594)

    _TAG_SETUP_WINDOW = "redditSetupWindow"
    _TAG_FORM_ISSUES_GROUP = "form_issuesGroup"
    _TAG_FORM_SUBREDDIT = "form_subreddit"
    _TAG_FORM_SOURCE = "form_source"
    _TAG_FORM_TIMEFRAME = "form_timeframe"
    _TAG_FORM_SUBMIT = "form_submit"

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
        # Create the setup window
        with dpg.window(
            label="Subreddit Selection",
            tag=self._TAG_SETUP_WINDOW,
            width=self.SIZE_SETUP[0],
            height=self.SIZE_SETUP[1],
            autosize=True,
            no_close=True
        ):
            # Add instructions
            dpg.add_text("Select a subreddit to browse and what content to view.")

            # Add the issues group
            dpg.add_child_window(tag=self._TAG_FORM_ISSUES_GROUP, show=False)

            # Add input fields
            dpg.add_input_text(label="Subreddit", hint="r/pics", tag=self._TAG_FORM_SUBREDDIT)
            dpg.add_combo(label="Source", items=[src.value for src in PostSource], default_value=PostSource.HOT.value, tag=self._TAG_FORM_SOURCE)
            dpg.add_combo(label="Timeframe", items=[time.value for time in PostTime], default_value=PostTime.DAY.value, tag=self._TAG_FORM_TIMEFRAME)

            # Add the submit button
            dpg.add_button(label="Submit", tag=self._TAG_FORM_SUBMIT, callback=self.__submitFormCallback)

    # Callback Functions
    def __submitFormCallback(self, sender: Union[int, str]):
        """
        Handles form submission.

        sender: The sender's tag.
        """
        pass # TODO: this

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
