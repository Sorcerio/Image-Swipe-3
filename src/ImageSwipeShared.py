# Image Swipe 3: Image Swipe
# Shared functionality for Image Swipe 3.

# Imports
import os
import dearpygui.dearpygui as dpg
from typing import Union, Optional, Callable, Any

# Functions
def fullpath(path: str) -> str:
    """
    Returns the full path of the given path.

    path: The path to convert to a full path.
    """
    return os.path.abspath(os.path.expandvars(path))

def createModal(title: str, tag: Union[str, int], content: Callable[[Any, ], None], data: Optional[Any] = None, canClose: bool = True):
    """
    Creates and presents a model window belonging to the given parent.

    title: The title of the modal window.
    tag: The tag the modal should identify as.
    content: A function that declares the `dearpygui` elements for the modal. Must have at least one argument to receive `data`.
    data: Any data to pass to the content function.
    canClose: Whether the modal can be closed by the user using the window's "x" button.
    """
    # Ensure same frame
    with dpg.mutex():
        # Get the viewport size
        viewportSize = (
            dpg.get_viewport_client_width(),
            dpg.get_viewport_client_height()
        )

        # Add the Add Modal
        with dpg.window(
            label=title,
            modal=True,
            autosize=True,
            tag=tag,
            no_close=(not canClose),
            on_close=(lambda: dpg.delete_item(tag))
        ):
            # Build the content
            content(data)

    # Execute on the next frame
    dpg.split_frame()

    # Get the alert size
    alertSize = (
        dpg.get_item_width(tag),
        dpg.get_item_height(tag)
    )

    # Center the window
    dpg.set_item_pos(tag, (
        ((viewportSize[0] // 2) - (alertSize[0] // 2)),
        ((viewportSize[1] // 2) - (alertSize[1] // 2))
    ))

def createConfirmationModal(
    title: str,
    message: str,
    confirmText: str = "Confirm",
    cancelText: str = "Cancel",
    onConfirm: Optional[Callable[[], None]] = None,
    onCancel: Optional[Callable[[], None]] = None
):
    """
    Creates a confirmation modal window.

    title: The title of the modal window.
    message: The message to display to the user.
    confirmText: The text to display on the confirm button.
    cancelText: The text to display on the cancel button.
    onConfirm: The function to call when the user confirms.
    onCancel: The function to call when the user cancels.
    """
    # Prepare a tag
    tag = dpg.generate_uuid()

    # Prepare the callback functions
    def triggerConfirm(sender: Union[int, str]):
        # Check if the confirm function is provided
        if onConfirm is not None:
            onConfirm()

        # Close the modal
        dpg.delete_item(tag)

    def triggerCancel(sender: Union[int, str]):
        # Check if the cancel function is provided
        if onCancel is not None:
            onCancel()

        # Close the modal
        dpg.delete_item(tag)

    # Prepare the content function
    def confirmationContent(data: Any):
        # Add the text
        dpg.add_text(message)

        # Add the buttons
        with dpg.group(horizontal=True):
            dpg.add_button(label=confirmText, callback=triggerConfirm)
            dpg.add_button(label=cancelText, callback=triggerCancel)

    # Create the modal
    createModal(
        title,
        tag,
        confirmationContent,
        canClose=False
    )

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
