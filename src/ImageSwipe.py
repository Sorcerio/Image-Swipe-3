# Image Swipe 3: Image Swipe
# Core interface runner for Image Swipe 3.

# Imports
import os
from typing import Union, Optional
import dearpygui.dearpygui as dpg

from .ImageSwipeShared import ASSETS_DIR, fullpath, createConfirmationModal
from .PercentageLayout import PercentageLayout
from .TextureManager import TextureManager

# Classes
class ImageSwipe:
    """
    Core interface runner for Image Swipe 3.
    """
    # Constants
    _PATH_ICON_SMALL = fullpath(os.path.join(ASSETS_DIR, "icon_32.ico"))
    _PATH_ICON_LARGE = fullpath(os.path.join(ASSETS_DIR, "icon_128.ico"))

    _TAG_WINDOW_MAIN = "mainWindow"

    # Constructor
    def __init__(self, debug: bool = False):
        """
        debug: If `True`, debug features will be enabled.
        """
        # Assign data
        self.debug = debug
        self._primaryWindowsPresented = False

        # Prepare sub objects
        self._textures: Optional[TextureManager] = None

        # Image check
        if not os.path.exists(self._PATH_ICON_SMALL):
            print(f"No small icon file at: {self._PATH_ICON_SMALL}")

        if not os.path.exists(self._PATH_ICON_LARGE):
            print(f"No large icon file at: {self._PATH_ICON_LARGE}")

    # Functions
    def display(self):
        """
        Displays the Image Swipe GUI.
        """
        # Prepare the interface context
        dpg.create_context()
        dpg.create_viewport(
            title="Image Swipe 3",
            small_icon=self._PATH_ICON_SMALL,
            large_icon=self._PATH_ICON_LARGE
        )
        dpg.setup_dearpygui()

        # Setup the texture manager
        self._textures = TextureManager()

        # Add main toolbar
        self._buildToolbar()

        # Build main window
        self._buildMainWindow()

        # Show the interface
        dpg.show_viewport()

        # Set the primary window
        dpg.set_primary_window(self._TAG_WINDOW_MAIN, True)

        # Start the interface with a render loop
        while dpg.is_dearpygui_running():
            # Check if the primary windows are presented
            if self._primaryWindowsPresented:
                pass

            # Render the frame
            dpg.render_dearpygui_frame()

        # Cleanup the interface context
        dpg.destroy_context()

    # UI Functions
    def _buildToolbar(self):
        """
        Builds the primary window toolbar.
        """
        # Add top menu bar
        with dpg.viewport_menu_bar(parent=self._TAG_WINDOW_MAIN):
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Quit", callback=self.__toolbarQuitCallback)

            if self.debug:
                with dpg.menu(label="Debug"):
                    dpg.add_menu_item(label="Performance Metrics", callback=(lambda : dpg.show_tool(dpg.mvTool_Metrics)))
                    dpg.add_menu_item(label="Item Registry", callback=(lambda : dpg.show_tool(dpg.mvTool_ItemRegistry)))
                    dpg.add_menu_item(label="Style Editor", callback=(lambda : dpg.show_tool(dpg.mvTool_Style)))
                    dpg.add_menu_item(label="Texture Registry", callback=(lambda : self._textures.showTextureRegistry()))

    def __toolbarQuitCallback(self, sender: Union[int, str]):
        """
        Callback for when the user selects to quit from the toolbar.

        sender: The tag of the sender.
        """
        # Confirm quit
        createConfirmationModal(
            "Quit",
            "Are you sure you want to quit?",
            confirmText="Quit",
            cancelText="Go Back",
            onConfirm=(lambda : dpg.stop_dearpygui())
        )

    def _buildMainWindow(self):
        """
        Builds the main window.
        """
        # Define sizing
        sTopSpacer = 10
        sButtonH = 64
        sSpacer = 8

        # Add main window
        with dpg.window(tag=self._TAG_WINDOW_MAIN):
            # Add toolbar spacer
            dpg.add_spacer(height=sTopSpacer)

            # Add the image display
            dpg.add_image(self._textures._TAG_IMAGE_ERROR) # TODO: dynamic!

            # Add the buttons
            with dpg.group(horizontal=True): # TODO: Allow button configuration
                # Prepare percentage layout
                layout = PercentageLayout()

                # Add the buttons
                layout.addItem(dpg.add_button(label="Discard", height=sButtonH), 33)
                layout.addItem(dpg.add_button(label="Favorite", height=sButtonH), 34)
                layout.addItem(dpg.add_button(label="Save", height=sButtonH), 33)

                # Apply the layout
                layout.apply()

        # Flag as presented
        self._primaryWindowsPresented = True

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
