# Image Swipe 3: Texture Model
# Data object for handling texture data.

# Imports
from typing import Union, Optional

import dearpygui.dearpygui as dpg

# Classes
class TextureModel:
    """
    Data object for handling texture data.
    """
    # Constructor
    def __init__(self, filepath: str, tag: Union[int, str] = None, label: Optional[str] = None):
        """
        filepath: The path to the image to use for the texture.
        tag: An explicit tag to associated with the texture. If `None`, a unique UUID will be generated.
        label: A text label to associate with the image. If not provided, the `tag` will be used.
        """
        self.filepath = filepath
        self.tag = (tag or dpg.generate_uuid())
        self.label = (label or self.tag)

    # Python Functions
    def __repr__(self) -> str:
        return f"TextureModel({self.filepath}, {self.tag}, {self.label})"

    def __str__(self) -> str:
        return f"TextureModel({self.filepath}, {self.tag}, {self.label})"

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
