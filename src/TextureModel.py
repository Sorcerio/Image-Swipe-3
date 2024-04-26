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
        tag: The tag associated with the texture.
        """
        self.filepath = filepath
        self.tag = tag
        self.label = (label or tag)

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
