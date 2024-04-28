# Image Swipe 3: Image Swipe
# Core interface runner for Image Swipe 3.

# Imports
import os
import shutil
from typing import Union, Optional, Iterable, Callable, Any
from random import choice
import dearpygui.dearpygui as dpg

from .ImageSwipeShared import ASSETS_DIR, fullpath, createConfirmationModal
from .PercentageLayout import PercentageLayout
from .TextureManager import TextureManager
from .TextureModel import TextureModel
from .ActionButtonModel import ActionButtonModel, RejectButtonModel, AcceptButtonModel, HighlightButtonModel
from .HotkeyManager import Hotkey, HotkeySet, HotkeyManager

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
    _TAG_WINDOW_QUEUE = "queueWindow"
    _TAG_GROUP_IMAGES = "imageDisplayGroup"
    _TAG_PRIMARY_IMAGE = "primaryImage"
    _TAG_GROUP_CONTROLS = "controlsGroup"
    _TAG_GROUP_QUEUE_CONTENT = "queueContent"

    # Constructor
    def __init__(self,
        outputDir: str,
        buttons: Optional[list[ActionButtonModel]] = None,
        hotkeys: Optional[list[HotkeySet]] = None,
        preloadBuffer: int = 3,
        debug: bool = False
    ):
        """
        outputDir: The directory to place output directories in.
        buttons: The buttons to display on the interface.
        hotkeys: A list of `HotkeySet` objects defining additional hotkey actions to register with the interface.
        preloadBuffer: The number of images to preload following the current image.
        debug: If `True`, debug features will be enabled.
        """
        # Assign data
        self.debug = debug
        self.outputDir = fullpath(outputDir)
        self.preloadBuffer = preloadBuffer

        if buttons is None:
            # Prepare default buttons
            self._buttons = [
                RejectButtonModel(),
                HighlightButtonModel(),
                AcceptButtonModel()
            ]

            # Check if debug
            if debug:
                print("Using default buttons.")
        else:
            # Use provided buttons
            self._buttons = buttons

            # Check if debug
            if debug:
                print("Using provided buttons.")

        self.__curImageIndex = 0
        self._images: list[TextureModel] = []

        self._primaryWindowsPresented = False
        self.__onFirstFrameTriggered = False

        # Prepare texture manager
        self._textureManager: Optional[TextureManager] = None

        # Prepare hotkey manager
        self._hotkeyManager: Optional[HotkeyManager]
        if buttons is None:
            # Load default hotkeys
            self._hotkeyManager = HotkeyManager((
                HotkeySet(
                    "Swipe Controls",
                    (
                        Hotkey((dpg.mvKey_Left, ), "Discard image", (lambda _ : self._triggerButtonAction(RejectButtonModel()))),
                        Hotkey((dpg.mvKey_Up, ), "Favorite image", (lambda _ : self._triggerButtonAction(HighlightButtonModel()))),
                        Hotkey((dpg.mvKey_Right, ), "Keep image", (lambda _ : self._triggerButtonAction(AcceptButtonModel()))),
                        Hotkey((dpg.mvKey_Back, ), "Previous image", (lambda _ : self._showPrevImage())),
                    )
                ), )
            )

            # Check if debug
            if debug:
                print("Using default hotkeys.")
        elif hotkeys is not None:
            # Load only provided hotkeys
            self._hotkeyManager = HotkeyManager(hotkeys)

            # Check if debug
            if debug:
                print("Using provided hotkeys.")
        else:
            # Load no hotkeys
            self._hotkeyManager = None

            # Check if debug
            if debug:
                print("Hotkeys are disabled.")

        # Image check
        if not os.path.exists(self._PATH_ICON_SMALL):
            print(f"No small icon file at: {self._PATH_ICON_SMALL}")

        if not os.path.exists(self._PATH_ICON_LARGE):
            print(f"No large icon file at: {self._PATH_ICON_LARGE}")

    # Functions
    def display(self, onFirstFrame: Optional[Callable[[None], None]] = None):
        """
        Displays the Image Swipe GUI.

        onFirstFrame: A function to call on the first frame after displaying the interface.
        """
        # Prepare the interface context
        dpg.create_context()
        dpg.create_viewport(
            title="Image Swipe 3",
            small_icon=self._PATH_ICON_SMALL,
            large_icon=self._PATH_ICON_LARGE
        )
        dpg.setup_dearpygui()

        # Setup the hotkeys
        if self._hotkeyManager is not None:
            self._hotkeyManager.registerHotkeys()

        # Set the viewport resize callback
        dpg.set_viewport_resize_callback(self.__viewportResizedCallback)

        # Setup the texture manager
        self._textureManager = TextureManager()

        # Add main toolbar
        self._buildToolbar()

        # Build core windows
        self._buildMainWindow()
        self._buildQueueWindow()

        # Show the interface
        dpg.show_viewport()

        # Set the primary window
        dpg.set_primary_window(self._TAG_WINDOW_MAIN, True)

        # Start the interface with a render loop
        while dpg.is_dearpygui_running():
            # Check if the first frame has been triggered
            if not self.__onFirstFrameTriggered:
                # Trigger the first frame
                if onFirstFrame is not None:
                    onFirstFrame()

                # Flag as triggered
                self.__onFirstFrameTriggered = True

            # Check if the primary windows are presented
            if self._primaryWindowsPresented:
                pass

            # Render the frame
            dpg.render_dearpygui_frame()

        # Cleanup the interface context
        dpg.destroy_context()

    def addImageToQueue(self, image: TextureModel):
        """
        Adds an image to the queue for presentation.

        image: A `TextureModel` object to add to the queue.
        """
        # Add to list
        self._images.append(image)

    def addImagesToQueue(self, images: Iterable[TextureModel]):
        """
        Adds a list of images to the queue for presentation.

        images: An iterable of `TextureModel` objects to add to the queue.
        """
        # Add to list
        self._images.extend(images)

    def startQueue(self):
        """
        Presents the first image in the queue.
        """
        # Set to the first image
        self.__curImageIndex = 0

        # Update the texture cache
        self._updateTextureCache()

        # Present the image
        self._presentImage(self._images[self.__curImageIndex].tag)

    # UI Functions
    def _buildToolbar(self):
        """
        Builds the primary window toolbar.
        """
        # Add top menu bar
        with dpg.viewport_menu_bar(parent=self._TAG_WINDOW_MAIN):
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Quit", callback=self.__toolbarQuitCallback)

            with dpg.menu(label="View"):
                dpg.add_menu_item(label="Image Queue", callback=self.__toolbarShowQueueCallback)

            if self._hotkeyManager is not None:
                self._hotkeyManager.buildToolbar()

            if self.debug:
                with dpg.menu(label="Debug"):
                    dpg.add_menu_item(label="Performance Metrics", callback=(lambda : dpg.show_tool(dpg.mvTool_Metrics)))
                    dpg.add_menu_item(label="Item Registry", callback=(lambda : dpg.show_tool(dpg.mvTool_ItemRegistry)))
                    dpg.add_menu_item(label="Style Editor", callback=(lambda : dpg.show_tool(dpg.mvTool_Style)))
                    dpg.add_menu_item(label="Texture Registry", callback=(lambda : self._textureManager.showTextureRegistry()))
                    dpg.add_separator()
                    dpg.add_menu_item(label="Display Random Image", callback=(lambda : self._presentImage(choice(self._textureManager._textures))))

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
            with dpg.group(horizontal=True, tag=self._TAG_GROUP_CONTROLS):
                # Prepare percentage layout
                layout = PercentageLayout()

                # Add the buttons
                btnPerc = (100 // len(self._buttons))
                for btn in self._buttons:
                    layout.addItem(dpg.add_button(
                        label=btn.label,
                        height=sButtonH,
                        user_data=btn,
                        callback=self.__controlButtonCallback
                    ), btnPerc)

                # Apply the layout
                layout.apply()

        # Flag as presented
        self._primaryWindowsPresented = True

    def _buildQueueWindow(self):
        """
        Builds the queue display window.
        """
        # Add queue window
        dpg.add_window(label="Image Queue", tag=self._TAG_WINDOW_QUEUE, show=False)

        # Update the queue window
        self._updateQueueWindow()

    def _updateQueueWindow(self):
        """
        Updates the content of the queue window.
        """
        # Remove the old content group
        dpg.delete_item(self._TAG_GROUP_QUEUE_CONTENT)

        # Add the content group
        with dpg.group(tag=self._TAG_GROUP_QUEUE_CONTENT, parent=self._TAG_WINDOW_QUEUE):
            # Add the count text
            dpg.add_text(f"Viewing Image: {self.__curImageIndex + 1} of {len(self._images)}")

            # Add the queue display
            with dpg.child_window():
                # Loop through the queue
                for i, image in enumerate(self._images): # TODO: Add to table with more info and skip-to button
                    # Check if current
                    if (i == self.__curImageIndex):
                        # Show text with current
                        dpg.add_text(f"(CURRENT) {i + 1}: {image.label}", bullet=True)
                    else:
                        # Show text
                        dpg.add_text(f"{i + 1}: {image.label}", bullet=True)

    def _updateTextureCache(self):
        """
        Updates the texture cache with the most relevant images based on current index.
        """
        # Check if the texture manager is ready
        if self._textureManager is None:
            raise ValueError("Texture Manager is not ready for input.")

        # Load the image before current
        if (self.__curImageIndex > 0):
            self._loadImageToCache(self._images[self.__curImageIndex - 1])

        # Load the current image
        self._loadImageToCache(self._images[self.__curImageIndex])

        # Load images after current for buffer length
        for i in range(1, self.preloadBuffer + 1):
            if (self.__curImageIndex + i < len(self._images)):
                self._loadImageToCache(self._images[self.__curImageIndex + i])

    def _loadImageToCache(self, image: TextureModel):
        """
        Loads the given image to the texture cache.

        image: The `TextureModel` object to load into the cache.
        """
        # Check if the texture manager is ready
        if self._textureManager is None:
            raise ValueError("Texture Manager is not ready for input.")

        # Check if the image is not in the cache
        if (image.tag not in self._textureManager._textures):
            # Load the image
            self._textureManager.registerTexture(image.filepath, image.tag, image.label)

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

        self.__imagesToSet = tuple(zip(contentTags, tags))

        # Wait for windows to size
        dpg.split_frame()

        # Add sized images
        padding = 10
        # for parent, tag in zip(contentTags, tags):
        for parent, tag in self.__imagesToSet:
            # Get the parent size
            parentSize = dpg.get_item_rect_size(parent)
            parentSize = (
                parentSize[0] - padding,
                parentSize[1] - padding
            )

            # Calculate best fit size
            fitSize, pasteOffset = TextureManager.calcBestFitSize(self._textureManager._sizes[tag], parentSize, True)
            leftPad = (parentSize[0] - fitSize[0]) // 2

            # Add the image
            dpg.add_image(tag, parent=parent, width=fitSize[0], height=fitSize[1], indent=leftPad)

        self.__imagesToSet = None

    def _showNextImage(self):
        """
        Shows the next image in the queue.
        """
        # Check that there is a next image
        if ((self.__curImageIndex + 1) > len(self._images)):
            # No next image
            # TODO: Show a message or something? Callback?
            return

        # Increment the index
        self.__curImageIndex += 1

        # Update the texture cache
        self._updateTextureCache()

        # Present the image
        self._presentImage(self._images[self.__curImageIndex].tag)

        # Update the queue window
        self._updateQueueWindow()

    def _showPrevImage(self):
        """
        Shows the previous image in the queue.
        """
        # Check that there is a previous image
        if ((self.__curImageIndex - 1) < 0):
            # No previous image
            return

        # Reduce the index
        self.__curImageIndex -= 1

        # Update the texture cache
        self._updateTextureCache()

        # Present the image
        self._presentImage(self._images[self.__curImageIndex].tag)

        # Update the queue window
        self._updateQueueWindow()

    def _saveCurrentImage(self, toPath: str):
        """
        Saves the current image to the given directory.

        toPath: The path to save the image to.
        """
        # Check if debug
        if self.debug:
            print(f"Saving image at index {self.__curImageIndex} to: {toPath}")

        # Make the output directory
        os.makedirs(os.path.dirname(toPath), exist_ok=True)

        # Copy the image to the output directory
        shutil.copy2(self._images[self.__curImageIndex].filepath, toPath) # TODO: Provide option for move instead of copy

    def _triggerButtonAction(self, btn: ActionButtonModel):
        """
        Triggers the action of the given button.

        btn: The `ActionButtonModel` object associated with the button.
        """
        # Decide on the button type
        if btn.action == ActionButtonModel.ACTION_REJECT:
            # Reject button
            self._showNextImage()
        elif btn.action == ActionButtonModel.ACTION_ACCEPT:
            # Accept button
            self._saveCurrentImage(os.path.join(
                self.outputDir,
                btn.dirName,
                os.path.basename(self._images[self.__curImageIndex].filepath)
            ))
            self._showNextImage()

        # Trigger the button action
        if btn.callback is not None:
            btn.callback()

    # Callbacks
    def __viewportResizedCallback(self, sender: Union[int, str], size: tuple[int, int, int, int]):
        """
        Callback for handling when the viewport is resized.

        sender: The tag of the viewport.
        size: The new size of the viewport as a tuple like `(width, height, client width, client height)`.
        """
        # TODO: if viewport is resized, present the current images again so they fit

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

    def __toolbarShowQueueCallback(self, sender: Union[int, str]):
        """
        Callback for when the user selects to show the queue from the toolbar.

        sender: The tag of the sender.
        """
        # Update the queue window
        self._updateQueueWindow()

        # Show the queue window
        dpg.show_item(self._TAG_WINDOW_QUEUE)

    def __controlButtonCallback(self, sender: Union[int, str], v: Any, btn: ActionButtonModel):
        """
        Callback for when a control button is pressed.

        sender: The tag of the sender.
        v: The value of the sender.
        btn: The `ActionButtonModel` object associated with the button.
        """
        self._triggerButtonAction(btn)

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
