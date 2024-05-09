# Image Swipe 3: Startup Command Line Interface
# Unified Command Line interface for Image Swipe 3.

# Imports
import argparse

from .implementations import *

# Classes
class ImageSwipeCli:
    """
    Unified Command Line interface for Image Swipe 3.
    """
    # Constants
    IMPLEMENTATIONS = [ # TODO: Audtomate populating this list
        SwipeLocal,
        SwipeLocalMulti,
        SwipeReddit
    ]

    # Functions
    def start(self):
        """
        Starts the Image Swipe 3 command line interface.
        """
        # Setup root parser
        self.parser = argparse.ArgumentParser(prog="Image Swipe 3", description="A tool for rapid sorting of images from static and dynamic sources.")

        # Setup subparsers
        self.subparsers = self.parser.add_subparsers(dest="command", title="commands")

        # Setup the implementations
        self.__buildSubparsers()

        # Get args
        self.options = self.parser.parse_args()

        # Check for debug
        if hasattr(self.options, "debug") and self.options.debug:
            print(f"CLI Options: {self.options}")

        # Start the interface
        self.__startInterface()

    # Private Functions
    def __buildSubparsers(self):
        """
        Builds the subparsers for the implementations.
        """
        # Setup the implementations
        for imp in self.IMPLEMENTATIONS:
            subparser = self.subparsers.add_parser(imp.CLI_PROG, help=imp.CLI_DESC)
            imp.buildParser(subparser)

    def __startInterface(self):
        """
        Starts the specified interface from the command line arguments.
        """
        # Choose matching implementation
        for imp in self.IMPLEMENTATIONS:
            if self.options.command == imp.CLI_PROG:
                imp.fromArgs(self.options).display()
                return

        # Invalid
        self.parser.print_help()

# Command Line
if __name__ == "__main__":
    cli = ImageSwipeCli()
    cli.start()
