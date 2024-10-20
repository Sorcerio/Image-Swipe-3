# Image Swipe 3: Addon Demo
# Image Swipe 3 implementation for demonstrating the use of addons.

# MARK: Imports
import argparse

from src.implementations import SwiperImplementation, SwipeLocal

# MARK: Classes
class SwipeAddonDemo(SwiperImplementation):
    # Constants
    CLI_PROG = "addondemo"
    CLI_DESC = "Demonstrates the use of addons. Has no functionality."

    # Functions
    def display(self):
        """
        Displays the local image swipe interface.
        """
        print("=" * 32)
        print("This is a demonstration of an addon implementation.")
        print("See the source code for `src/implementations/SwipeLocal.py` for more detailed usage of Image Swipe 3's features.")
        print("=" * 32)

    # Class Functions
    @classmethod
    def fromArgs(cls, args: argparse.Namespace) -> 'SwiperImplementation':
        """
        Creates a new instance of this implementation using the given command line arguments.

        args: The command line arguments to use.

        Returns the new instance.
        """
        return cls()

    # Static Functions
    @staticmethod
    def buildParser(parser: argparse.ArgumentParser):
        """
        Sets up the given command line parser with the required arguments for this implementation.

        parser: The parser to setup.
        """
        return
