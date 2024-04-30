# Image Swipe 3: Image Queue Window
# Window for managing the image queue.

# Imports
from typing import Callable
import dearpygui.dearpygui as dpg

from .TextureModel import TextureModel

# Classes
class ImageQueueWindow:
    """
    Window for managing the image queue.
    """
    # Constants
    _QUEUE_WINDOW_SIZE = (840, 580)

    _TAG_WINDOW_QUEUE = "queueWindow"
    _TAG_GROUP_QUEUE_CONTENT = "queueContent"

    # Functions
    def register(self):
        """
        Builds the Queue Window and registers it with DearPyGui.
        """
        # Add queue window
        dpg.add_window(
            label="Image Queue",
            tag=self._TAG_WINDOW_QUEUE,
            show=False,
            width=self._QUEUE_WINDOW_SIZE[0],
            height=self._QUEUE_WINDOW_SIZE[1]
        )

    def update(self, index: int, images: list[TextureModel]):
        """
        Forces the window to update the data it is displaying.

        index: The current index of the image being viewed.
        images: The list of images that make up the queue.
        """
        # Remove the old content group
        dpg.delete_item(self._TAG_GROUP_QUEUE_CONTENT)

        # Add the content group
        with dpg.group(tag=self._TAG_GROUP_QUEUE_CONTENT, parent=self._TAG_WINDOW_QUEUE):
            # Add the count text
            dpg.add_text(f"Viewing Image: {index + 1} of {len(images)}")

            # Add the queue display
            with dpg.child_window():
                # Loop through the queue
                for i, image in enumerate(images): # TODO: Add to table with more info and skip-to button
                    # Check if current
                    if (i == index):
                        # Show text with current
                        dpg.add_text(f"(CURRENT) {i + 1}: {image.label}", bullet=True)
                    else:
                        # Show text
                        dpg.add_text(f"{i + 1}: {image.label}", bullet=True)

    def display(self, index: int, images: list[TextureModel]):
        """
        Displays the Queue Window.

        index: The current index of the image being viewed.
        images: The list of images that make up the queue.
        """
        # Update the window
        self.update(index, images)

        # Show the window
        dpg.configure_item(self._TAG_WINDOW_QUEUE, show=True)

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")

