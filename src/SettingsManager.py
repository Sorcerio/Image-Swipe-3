# Image Swipe 3: Settings Manager
# Manager object for handling settings in an interface.

# Imports
from typing import Union, Optional, Any
import dearpygui.dearpygui as dpg

from .ImageSwipeShared import createModal

# Classes
class SettingsSection:
    """
    Interface for a section of settings in the Settings Modal.
    """
    # Constants
    IDENTIFIER = "__UNDEFINED_SECTION__"

    # Functions
    def display(self, owner: Optional[Union[int, str]] = None):
        """
        Displays the settings for the section.

        owner: The tag of the owner of the settings. If `None`, values reliant on the owner will be set to default.
        """
        raise NotImplementedError("This function must be implemented in a subclass.")

class SettingsModal: # TODO: Make settings persistent in a .ini file!
    """
    Manager object for handling settings in an interface.
    """
    # Constants
    TAG_WINDOW_SETTINGS = "settingsModal"
    TAG_CONTENT = "settingsModal_contentGroup"

    # Constructor
    def __init__(self, width: int = 420) -> None:
        """
        width: An explicit width to set the modal to. If `0`, the modal will be autosized.
        """
        # Prepare data
        self.width = width

        # Prepare sections
        self.__sectionOrder = []
        self.__sections = {}

    # Functions
    def present(self):
        """
        Presents the Settings Modal.
        """
        # Create the modal
        createModal("Settings", self.TAG_WINDOW_SETTINGS, self._buildContent)

    def close(self):
        """
        Closes the Settings Modal.
        """
        # Close the modal
        dpg.delete_item(self.TAG_WINDOW_SETTINGS)

    def getSettingsForSection(self, identifier: str) -> Optional[SettingsSection]:
        """
        Retrieves the settings for a specific section.

        identifier: The identifier to retrieve the associated `SettingsSection` object for.

        Returns the `SettingsSection` object associated with the given `identifier` or `None` if the section does not exist.
        """
        if identifier not in self.__sections:
            return None

        return self.__sections[identifier]

    # Interface Functions
    def _buildContent(self, d: Any):
        """
        Builds the content of the Settings Modal.

        d: The data passed to the modal. Unused.
        """
        # Add content group
        with dpg.group(tag=self.TAG_CONTENT, parent=self.TAG_WINDOW_SETTINGS, width=self.width):
            # Add info text
            dpg.add_text("Settings are saved automatically.")
            dpg.add_separator()

            # Add sections
            for section in self.__sectionOrder:
                # Add the section collapsible
                with dpg.collapsing_header(label=section):
                    # Display the section
                    self.__sections[section].display(owner=self.TAG_CONTENT)

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
