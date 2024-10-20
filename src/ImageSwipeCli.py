# Image Swipe 3: Startup Command Line Interface
# Unified Command Line interface for Image Swipe 3.

# Imports
import os
import argparse
from typing import Optional, Iterable

# from .implementations import *
from . import implementations as imps

# Classes
class ImageSwipeCli:
    """
    Unified Command Line interface for Image Swipe 3.
    """
    # Constructor
    def __init__(self, addImps: Optional[Iterable[imps.SwiperImplementation]] = None) -> None:
        """
        Creates the Image Swipe 3 command line interface.

        addImps: Additional implementations to include in the CLI.
        """
        # Assign variables
        self._parser: Optional[argparse.ArgumentParser] = None
        self._subparsers: Optional[argparse._SubParsersAction] = None
        self._options: Optional[argparse.Namespace] = None

        # Collect implementations
        self.imps: list[imps.SwiperImplementation] = []
        for name in dir(imps):
            obj = getattr(imps, name)
            if isinstance(obj, type) and issubclass(obj, imps.SwiperImplementation) and (obj != imps.SwiperImplementation):
                self.imps.append(obj)

        # Add additional implementations
        if addImps:
            self.imps.extend(addImps)

        # Alphabetize
        self.imps.sort(key=lambda imp: imp.CLI_PROG)

    # Functions
    def start(self):
        """
        Starts the Image Swipe 3 command line interface.
        """
        # Setup root parser
        self._parser = argparse.ArgumentParser(prog="Image Swipe 3", description="A tool for rapid sorting of images from static and dynamic sources.")

        # Setup subparsers
        self._subparsers = self._parser.add_subparsers(dest="command", title="progs")

        # Setup the implementations
        self.__buildSubparsers()

        # Get args
        self._options = self._parser.parse_args()

        # Check for debug
        if hasattr(self._options, "debug") and self._options.debug:
            print(f"Loaded {len(self.imps)} CLI implementations: {', '.join(imp.CLI_PROG for imp in self.imps)}")
            print(f"CLI Options: {self._options}")

        # Start the interface
        self.__startInterface()

    # Private Functions
    def __buildSubparsers(self):
        """
        Builds the subparsers for the implementations.
        """
        # Setup the implementations
        for imp in self.imps:
            subparser = self._subparsers.add_parser(imp.CLI_PROG, help=imp.CLI_DESC)
            imp.buildParser(subparser)

    def __startInterface(self):
        """
        Starts the specified interface from the command line arguments.
        """
        # Choose matching implementation
        for imp in self.imps:
            if self._options.command == imp.CLI_PROG:
                imp.fromArgs(self._options).display()
                return

        # Invalid
        self._parser.print_help()

# Command Line
if __name__ == "__main__":
    cli = ImageSwipeCli()
    cli.start()
