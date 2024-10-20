import os
import importlib

import src.implementations as sourceImps
from src.ImageSwipeCli import ImageSwipeCli

current_dir = os.path.dirname(__file__)

modules = [f[:-3] for f in os.listdir(current_dir) if f.endswith(".py") and f != "__init__.py"]

__all__ = []
for module in modules:
    # Import the module
    mod = importlib.import_module(f".{module}", package=__name__)

    # Iterate over all attributes of the module
    for attrName in tuple(set(dir(mod)) - set(dir(sourceImps))):
        attribute = getattr(mod, attrName)

        # Check if the attribute is a class
        if isinstance(attribute, type):
            # Add the class to the globals
            globals()[attrName] = attribute

            # Add the class name to __all__
            __all__.append(attrName)
