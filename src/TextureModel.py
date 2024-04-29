# Image Swipe 3: Texture Model
# Data object for handling texture data.

# Imports
from typing import Union, Optional

# Classes
class TextureModel:
    """
    Data object for handling texture data.
    """
    # Constructor
    def __init__(self, filepath: str, tag: Union[int, str], label: Optional[str] = None):
        """
        filepath: The path to the image to use for the texture.
        tag: The tag associated with the texture.
        """
        self.filepath = filepath
        self.tag = f"{tag}_tex"
        self.label = (label or self.tag)

    # Python Functions
    def __repr__(self) -> str:
        return f"TextureModel({self.filepath}, {self.tag}, {self.label})"

    def __str__(self) -> str:
        return f"TextureModel({self.filepath}, {self.tag}, {self.label})"

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
