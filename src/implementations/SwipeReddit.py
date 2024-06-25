# Image Swipe 3: Reddit Swipe
# Image Swipe 3 implementation for Reddit browsing.

# Imports
import os
import argparse
from enum import Enum
from typing import Union, Optional
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

class PostTimeframe(Enum):
    """
    The post timeframe for Reddit post requests.
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
    _TAG_FORM_ISSUES_SUBWINDOW = "form_issuesSubwindow"
    _TAG_FORM_ISSUES_GROUP = "form_issuesGroup"
    _TAG_FORM_SUBREDDIT = "form_subreddit"
    _TAG_FORM_SOURCE = "form_source"
    _TAG_FORM_TIMEFRAME = "form_timeframe"
    _TAG_FORM_SUBMIT = "form_submit"

    # Constructor
    def __init__(self,
        outputDir: str,
        subreddit: Optional[str] = None,
        source: Optional[PostSource] = None,
        timeframe: Optional[PostTimeframe] = None,
        perPageLimit: int = 3, # TODO: Set to 25?
        debug: bool = False
    ):
        """
        outputDir: The directory to place output directories in.
        subreddit: The subreddit to prefill into the intial startup form.
        source: The `PostSource` to prefill into the initial startup form.
        timeframe: The `PostTimeframe` to prefill into the initial startup form.
        perPageLimit: The maximum number of items to fetch per page.
        debug: If `True`, debug features will be enabled.
        """
        # Record info
        self.debug = debug
        self.subreddit: Optional[str] = subreddit
        self.source: Optional[PostSource] = source
        self.timeframe: Optional[PostTimeframe] = timeframe

        self.__lastPostId = None

        # Validate per page limit
        if perPageLimit < 1:
            print("Per Page Item Limit cannot be <1. Setting per page limit to 1.")
            self.perPageLimit = 1
        elif perPageLimit > 100:
            print("Per Page Item Limit cannot be >100. Setting per page limit to 100.")
            self.perPageLimit = 100
        else:
            self.perPageLimit = perPageLimit

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

    def fetchPage(self, afterPost: Optional[str] = None):
        """
        Fetches the given page of posts.

        afterPost: A post ID to fetch posts after.
        """
        # TODO: Fetch the page of posts, sort for ones with an image (or gallery), cache locally, and add to queue
        print(self.toRedditUrl(self.subreddit, self.source, self.timeframe, limit=self.perPageLimit))

    # Class Functions
    @classmethod
    def fromArgs(cls, args: argparse.Namespace) -> 'SwipeReddit':
        """
        Creates a new instance of this implementation using the given command line arguments.

        args: The command line arguments to use.

        Returns the new instance.
        """
        # Check if the subreddit is valid
        if (args.subreddit is not None) and (not args.subreddit.startswith("r/")):
            raise ValueError("Subreddit must start with \"r/\".")

        # Check if the source and timeframe are valid
        source = PostSource(args.source) if (args.source is not None) else None
        timeframe = PostTimeframe(args.timeframe) if (args.timeframe is not None) else None

        # Create the instance
        return cls(
            args.output,
            subreddit=args.subreddit,
            source=source,
            timeframe=timeframe,
            debug=args.debug
        )

    # Static Functions
    @staticmethod
    def buildParser(parser: argparse.ArgumentParser):
        """
        Sets up the given command line parser with the required arguments for this implementation.

        parser: The parser to setup.
        """
        # Add required arguments
        parser.add_argument("output", type=str, help="The directory to place output directories in.")

        # Add optional arguments
        parser.add_argument("-r", "--subreddit", help="A subreddit to prefill into the intial startup form.", type=str, default=None)
        parser.add_argument("-s", "--source", help="A source to prefill into the intial startup form.", type=str, choices=[c.name.lower() for c in PostSource], default=PostSource.HOT.name.lower())
        parser.add_argument("-t", "--timeframe", help="A timeframe to prefill into the intial startup form.", type=str, choices=[c.name.lower() for c in PostTimeframe], default=PostTimeframe.DAY.name.lower())
        parser.add_argument("--debug", help="If provided, enables debug mode.", action="store_true")

    @staticmethod
    def _validateForm(subreddit: str, source: PostSource, timeframe: PostTimeframe) -> Optional[list[str]]:
        """
        Validates the form.

        subreddit: The subreddit to validate.
        source: The `PostSource` source to validate.
        timeframe: The `PostTimeframe` timeframe to validate.

        Returns a list of errors or `None` if everything is valid.
        """
        # Prep errors
        errors = []

        # Check if the subreddit is valid
        if not subreddit.startswith("r/"):
            errors.append("Subreddit must start with \"r/\".")

        # Check if the source is valid
        if source not in PostSource:
            errors.append("Invalid source.")

        # Check if the timeframe is valid
        if timeframe not in PostTimeframe:
            errors.append("Invalid timeframe.")

        # Send the right thing
        if len(errors) > 0:
            return errors
        else:
            return None

    @staticmethod
    def toRedditUrl(
        subreddit: str,
        source: PostSource,
        timeframe: PostTimeframe,
        afterId: Optional[str] = None,
        limit: int = 25,
    ) -> str:
        """
        Produces a request URL for the given information.

        subreddit: The subreddit to request from including `r/`.
        source: The `PostSource` source to request from.
        timeframe: The `PostTimeframe` timeframe to request from.
        afterId: The ID of the post to request after for pagination. If `None`, pagination will start from the most recent post in the `timeframe`.
        limit: The maximum number of posts to return.

        Returns the request URL.
        """
        # Build the root url
        url = f"https://www.reddit.com/{subreddit}/{source.value}.json?t={timeframe.value}&count={limit}"

        # Check if an after ID is provided
        if afterId is not None:
            url += f"&after={afterId}"

        return url

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
            dpg.add_child_window(tag=self._TAG_FORM_ISSUES_SUBWINDOW, show=False, height=150)

            # Add input fields
            dpg.add_input_text(
                label="Subreddit",
                hint="r/pics",
                default_value=(self.subreddit if (self.subreddit is not None) else ""),
                tag=self._TAG_FORM_SUBREDDIT
            )
            dpg.add_combo(
                label="Source",
                items=[src.value for src in PostSource],
                default_value=(self.source.value if (self.source is not None) else PostSource.HOT.value),
                tag=self._TAG_FORM_SOURCE
            )
            dpg.add_combo(
                label="Timeframe",
                items=[time.value for time in PostTimeframe],
                default_value=(self.timeframe.value if (self.timeframe is not None) else PostTimeframe.DAY.value),
                tag=self._TAG_FORM_TIMEFRAME
            )

            # Add the submit button
            dpg.add_button(label="Submit", tag=self._TAG_FORM_SUBMIT, callback=self.__submitFormCallback)

    # Callback Functions
    def __submitFormCallback(self, sender: Union[int, str]):
        """
        Handles form submission.

        sender: The sender's tag.
        """
        # Get the form data
        subreddit = dpg.get_value(self._TAG_FORM_SUBREDDIT)
        source = PostSource(dpg.get_value(self._TAG_FORM_SOURCE))
        timeframe = PostTimeframe(dpg.get_value(self._TAG_FORM_TIMEFRAME))

        # Debug
        if self.debug:
            print(f"Subreddit: {subreddit}")
            print(f"Source: {source}")
            print(f"Timeframe: {timeframe}")

        # Validate the form
        if (errors := self._validateForm(subreddit, source, timeframe)) is not None:
            # Clear existing errors
            if dpg.does_item_exist(self._TAG_FORM_ISSUES_GROUP):
                dpg.delete_item(self._TAG_FORM_ISSUES_GROUP)

            # Show the issues subwindow
            dpg.show_item(self._TAG_FORM_ISSUES_SUBWINDOW)

            # Create the issues group
            with dpg.group(tag=self._TAG_FORM_ISSUES_GROUP, parent=self._TAG_FORM_ISSUES_SUBWINDOW):
                # Add the errors
                for error in errors:
                    dpg.add_text(error, bullet=True)

            # Debug
            if self.debug:
                print(f"Form input unsuccessful: {', '.join(errors)}")

            # Eject
            return

        # Close the setup window
        dpg.hide_item(self._TAG_FORM_ISSUES_SUBWINDOW)
        dpg.hide_item(self._TAG_SETUP_WINDOW)

        # Record the inputs
        self.subreddit = subreddit
        self.source = source
        self.timeframe = timeframe

        # Fetch the first page
        self.fetchPage()

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
