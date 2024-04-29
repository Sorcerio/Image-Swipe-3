# Image Swipe 3: Action Button Model
# Data object for defining action buttons.

# Imports
from typing import Optional, Callable, Any
from .ImageSwipeShared import sanitizeFileName

# Classes
class ActionButtonModel:
    """
    Data object for defining action buttons.
    """
    # Constants
    ACTION_REJECT = "reject"
    ACTION_ACCEPT = "accept"
    ACTION_CUSTOM = "custom"

    # Constructor
    def __init__(self, label: str, action: str, callback: Optional[Callable[[Any], None]] = None, userData: Any = None):
        """
        label: The text displayed on the button and is used to determine output directory name.
        action: The default action to perform when the button is clicked.
        callback: The function to call when the button is clicked. This is run in addition to the button's default behavior. Must accept a single argument for the `userData`.
        userData: Any additional data to associate with the button. This is returned in the `callback` if one is provided.
        """
        self.label = label
        self.action = action
        self.dirName = sanitizeFileName(label)
        self.callback = callback
        self.userData = userData

class RejectButtonModel(ActionButtonModel):
    """
    Data object for defining a Reject action button.
    """
    # Constructor
    def __init__(self, label: str = "Discard", callback: Optional[Callable[[Any], None]] = None, userData: Any = None):
        """
        label: The text displayed on the button and is used to determine output directory name.
        callback: The function to call when the button is clicked. This is run in addition to the button's default behavior. Must accept a single argument for the `userData`.
        userData: Any additional data to associate with the button. This is returned in the `callback` if one is provided.
        """
        super().__init__(label, ActionButtonModel.ACTION_REJECT, callback=callback, userData=userData)

class AcceptButtonModel(ActionButtonModel):
    """
    Data object for defining an Accept action button.
    """
    # Constructor
    def __init__(self, label: str = "Keep", callback: Optional[Callable[[Any], None]] = None, userData: Any = None):
        """
        label: The text displayed on the button and is used to determine output directory name.
        callback: The function to call when the button is clicked. This is run in addition to the button's default behavior. Must accept a single argument for the `userData`.
        userData: Any additional data to associate with the button. This is returned in the `callback` if one is provided.
        """
        super().__init__(label, ActionButtonModel.ACTION_ACCEPT, callback=callback, userData=userData)

class HighlightButtonModel(ActionButtonModel):
    """
    Data object for defining a Highlight action button.
    """
    # Constructor
    def __init__(self, label: str = "Favorite", callback: Optional[Callable[[Any], None]] = None, userData: Any = None):
        """
        label: The text displayed on the button and is used to determine output directory name.
        callback: The function to call when the button is clicked. This is run in addition to the button's default behavior. Must accept a single argument for the `userData`.
        userData: Any additional data to associate with the button. This is returned in the `callback` if one is provided.
        """
        super().__init__(label, ActionButtonModel.ACTION_ACCEPT, callback=callback, userData=userData)

class CustomButtonModel(ActionButtonModel):
    """
    Data object for defining a Custom action button.
    """
    # Constructor
    def __init__(self, label: str, callback: Optional[Callable[[Any], None]], userData: Any = None):
        """
        label: The text displayed on the button and is used to determine output directory name.
        callback: The function to call when the button is clicked. This is run in addition to the button's default behavior. Must accept a single argument for the `userData`.
        userData: Any additional data to associate with the button. This is returned in the `callback` if one is provided.
        """
        super().__init__(label, ActionButtonModel.ACTION_CUSTOM, callback=callback, userData=userData)

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
