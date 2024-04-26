# Image Swipe 3: Action Button Model
# Data object for defining action buttons.

# Imports
from typing import Union, Optional, Callable

# Classes
class ActionButtonModel:
    """
    Data object for defining action buttons.
    """
    # Constants
    ACTION_REJECT = "reject"
    ACTION_ACCEPT = "accept"
    ACTION_HIGHLIGHT = "highlight"
    ACTION_NOTHING = "nothing"

    # Constructor
    def __init__(self, label: str, action: str, dirName: Optional[str] = None, callback: Optional[Callable[[None], None]] = None):
        """
        tag: The tag associated with the texture.
        action: The default action to perform when the button is clicked.
        dirName: The name of the directory that should be made in the relevant output directory if saving items related to this button.
        callback: The function to call when the button is clicked. This is run in addition to the button's default behavior.
        """
        self.label = label
        self.action = action
        self.dirName = dirName
        self.callback = callback

class RejectButtonModel(ActionButtonModel):
    """
    Data object for defining a Reject action button.
    """
    # Constructor
    def __init__(self, label: str = "Discard", callback: Optional[Callable[[None], None]] = None):
        """
        tag: The tag associated with the texture.
        callback: The function to call when the button is clicked. This is run in addition to the button's default behavior.
        """
        super().__init__(label, ActionButtonModel.ACTION_REJECT, dirName=None, callback=callback)

class AcceptButtonModel(ActionButtonModel):
    """
    Data object for defining an Accept action button.
    """
    # Constructor
    def __init__(self, label: str = "Keep", callback: Optional[Callable[[None], None]] = None):
        """
        tag: The tag associated with the texture.
        callback: The function to call when the button is clicked. This is run in addition to the button's default behavior.
        """
        super().__init__(label, ActionButtonModel.ACTION_ACCEPT, dirName="Keep", callback=callback)

class HighlightButtonModel(ActionButtonModel):
    """
    Data object for defining a Highlight action button.
    """
    # Constructor
    def __init__(self, label: str = "Highlight", callback: Optional[Callable[[None], None]] = None):
        """
        tag: The tag associated with the texture.
        callback: The function to call when the button is clicked. This is run in addition to the button's default behavior.
        """
        super().__init__(label, ActionButtonModel.ACTION_HIGHLIGHT, dirName="Favorite", callback=callback)

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
