# Image Swipe 3: Local Image Swipe
# Image Swipe 3 implementation for local image sorting.

# Imports
from ..ImageSwipeCore import ImageSwipeCore
from ..ActionButtonModel import ActionButtonModel, RejectButtonModel, AcceptButtonModel, HighlightButtonModel

# Classes
class SwipeLocal:
    """
    Image Swipe 3 implementation for local image sorting.
    """
    # Constructor
    def __init__(self, inputDir: str, outputDir: str, debug: bool = False):
        """
        inputDir: The directory to load images from.
        outputDir: The directory to 
        debug: If `True`, debug features will be enabled.
        """
        # Prepare the core
        self.core = ImageSwipeCore(
            debug=debug
        )

    # Functions
    def display(self):
        """
        Displays the local image swipe interface.
        """
        # Display the core
        self.core.display()

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
