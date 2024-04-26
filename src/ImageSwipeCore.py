# Image Swipe 3: Image Swipe
# Core interface runner for Image Swipe 3.

# Imports
import os
from typing import Union, Optional
from random import choice
import dearpygui.dearpygui as dpg

from .ImageSwipeShared import ASSETS_DIR, fullpath, createConfirmationModal
from .PercentageLayout import PercentageLayout
from .TextureManager import TextureManager

# Classes
class ImageSwipeCore:
    """
    Core interface runner for Image Swipe 3.
    """
    # Constants
    _PATH_ICON_SMALL = fullpath(os.path.join(ASSETS_DIR, "icon_32.ico"))
    _PATH_ICON_LARGE = fullpath(os.path.join(ASSETS_DIR, "icon_128.ico"))

    _TAG_WINDOW_MAIN = "mainWindow"
    _TAG_WINDOW_IMAGE = "imageDisplay"
    _TAG_GROUP_IMAGES = "imageDisplayGroup"
    _TAG_PRIMARY_IMAGE = "primaryImage"
    _TAG_GROUP_CONTROLS = "controlsGroup"

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

        # Set the viewport resize callback
        dpg.set_viewport_resize_callback(self.__viewportResizedCallback)

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
                    dpg.add_separator()
                    dpg.add_menu_item(label="Display Random Image", callback=(lambda : self._presentImage(choice(self._textures._textures))))

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
        sTopSpacer = 15
        sButtonH = 64
        sSpacer = 8

        # Add main window
        with dpg.window(tag=self._TAG_WINDOW_MAIN):
            # Add toolbar spacer
            dpg.add_spacer(height=sTopSpacer)

            # Add the image display
            with dpg.child_window(
                width=-1,
                height=-(sButtonH + sSpacer),
                tag=self._TAG_WINDOW_IMAGE,
                no_scrollbar=True,
                no_scroll_with_mouse=True
            ):
                # Add the image display group
                dpg.add_group(tag=self._TAG_GROUP_IMAGES)

            # Add the buttons
            with dpg.group(horizontal=True, tag=self._TAG_GROUP_CONTROLS): # TODO: Allow button configuration
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

    def _presentImage(self, tags: Union[list[Union[int, str]], tuple[Union[int, str], ...], Union[int, str]]):
        """
        Presents the image with the given tag.

        tag: The tag, or a iterable of tags, of the textures to present.
        """
        # Check if dearpygui is running
        if not dpg.is_dearpygui_running():
            print(f"Cannot present the following textures while the interface is not running: {', '.join(tags)}")
            return

        # Check if the tag is a single tag
        if not isinstance(tags, (list, tuple)):
            tags = (tags, )

        # Reset the image group
        dpg.delete_item(self._TAG_GROUP_IMAGES)
        dpg.add_group(tag=self._TAG_GROUP_IMAGES, parent=self._TAG_WINDOW_IMAGE)

        # Prepare the layout
        layout = PercentageLayout(parent=self._TAG_GROUP_IMAGES)

        # Add the image containers
        segmentSize = (100 // len(tags))
        for tag in tags:
            layout.addItem(dpg.add_child_window(border=False), segmentSize)

        # Apply the layout
        contentTags = layout.apply()

        # Wait for windows to size
        dpg.split_frame()

        # Add sized images
        padding = 10
        for parent, tag in zip(contentTags, tags):
            # Get the parent size
            parentSize = dpg.get_item_rect_size(parent)
            parentSize = (
                parentSize[0] - padding,
                parentSize[1] - padding
            )

            # Calculate best fit size
            fitSize, pasteOffset = TextureManager.calcBestFitSize(self._textures._sizes[tag], parentSize, True)
            leftPad = (parentSize[0] - fitSize[0]) // 2

            # Add the image
            dpg.add_image(tag, parent=parent, width=fitSize[0], height=fitSize[1], indent=leftPad)

    # Callbacks
    def __viewportResizedCallback(self, sender: Union[int, str], size: tuple[int, int, int, int]):
        """
        Callback for handling when the viewport is resized.

        sender: The tag of the viewport.
        size: The new size of the viewport as a tuple like `(width, height, client width, client height)`.
        """
        # TODO: if viewport is resized, present the current images again so they fit

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
