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
    def __init__(self) -> None:
        # Prepare layout base
        self._tableTag = dpg.add_table(header_row=False, policy=dpg.mvTable_SizingStretchProp)
        self._stageTag = dpg.add_stage()

        # Add to stack
        dpg.push_container_stack(self._stageTag)

    # Functions
    def addItem(self, tag: Union[int, str], perc: float):
        """
        Adds a DearPyGui item to the layout.

        tag: The tag of the item to add to the layout.
        perc: The percentage of the layout that the item should occupy.
        """
        # Add item
        dpg.add_table_column(init_width_or_weight=(perc / 100), parent=self._tableTag)
        dpg.set_item_width(tag, -1)

    def apply(self):
        """
        Applies the layout to the DearPyGui stage.
        """
        # Pop the stage
        dpg.pop_container_stack()
        with dpg.table_row(parent=self._tableTag):
            dpg.unstage(self._stageTag)

# Command line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
