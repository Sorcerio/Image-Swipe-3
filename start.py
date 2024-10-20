# Image Swipe 3: Command Line
# Command Line execution for Image Swipe 3.

# Imports
import addons
from src import ImageSwipeCli

# Command Line
if __name__ == "__main__":
    # Collect any addon implementations
    addonImps = ImageSwipeCli.getImpsFromModule(addons)

    # Start the CLI
    cli = ImageSwipeCli(addImps=addonImps)
    cli.start()
