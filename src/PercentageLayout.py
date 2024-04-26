# Image Swipe 3: Percentage Layout
# Helper class for managing percentage based layouts in DearPyGui.

# Based on code provided in the DearPyGui repo: https://github.com/hoffstadt/DearPyGui/discussions/1306
# Why isn't this just implemented by default?

# Imports
from typing import Union
import dearpygui.dearpygui as dpg

# Classes
class PercentageLayout:
    """
    Helper class for managing percentage based layouts in DearPyGui.

    Usage:
    ```Python
    layout = PercentageLayout()
    layout.addItem(dpg.add_button(label="50%"), 50)
    layout.addItem(dpg.add_button(label="50%"), 50)
    layout.apply()
    ```
    """
    # Constructor
    def __init__(self, parent: Union[int, str] = 0) -> None:
        """
        Creates the context for the layout.

        parent: The tag of the parent to add the layout to.
        """
        # Prepare layout base
        self._tableTag = dpg.add_table(header_row=False, policy=dpg.mvTable_SizingStretchProp, parent=parent)
        self._contentTags: list[Union[int, str]] = []
        self._stageTag = dpg.add_stage()

        # Add to stack
        dpg.push_container_stack(self._stageTag)

    # Functions
    def addItem(self, tag: Union[int, str], perc: float):
        """
        Adds a DearPyGui item to the layout.
        If called multiple times, items will be displayed from left to right.

        tag: The tag of the item to add to the layout.
        perc: The percentage of the layout that the item should occupy.
        """
        # Add item
        dpg.add_table_column(init_width_or_weight=(perc / 100), parent=self._tableTag)
        dpg.set_item_width(tag, -1)

        # Record the content tag
        self._contentTags.append(tag)

    def apply(self) -> tuple[Union[int, str], ...]:
        """
        Applies the layout to the DearPyGui stage.

        Returns a tuple of the content tags from left to right.
        """
        # Pop the stage
        dpg.pop_container_stack()
        with dpg.table_row(parent=self._tableTag):
            dpg.unstage(self._stageTag)

        # Return the content tags
        return tuple(self._contentTags)

# Command line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
