# Image Swipe 3: Image Swipe Implementation
# Super class for creating Image Swipe 3 implementations.

# Imports
import argparse

# Classes
class SwiperImplementation:
    """
    Super class for creating Image Swipe 3 implementations.
    """
    # Constants
    CLI_PROG = "default_prog"
    CLI_DESC = "an_empty_description"

    # Functions
    def display(self):
        """
        Displays the local image swipe interface.
        """
        raise NotImplementedError("This implementation does not support a user interface.")

    # Static Functions
    @classmethod
    def fromArgs(cls, args: argparse.Namespace) -> 'SwiperImplementation':
        """
        Creates a new instance of this implementation using the given command line arguments.

        args: The command line arguments to use.

        Returns the new instance.
        """
        raise NotImplementedError("This implementation does not support creation from command line arguments.")

    @staticmethod
    def buildParser(parser: argparse.ArgumentParser):
        """
        Sets up the given command line parser with the required arguments for this implementation.

        parser: The parser to setup.
        """
        raise NotImplementedError("This implementation does not support command line usage.")

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
