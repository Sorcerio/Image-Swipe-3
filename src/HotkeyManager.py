# Image Swipe 3: Hotkey Manager
# Classes for handling hotkeys.

# Imports
from typing import Callable, Iterable, Union
import dearpygui.dearpygui as dpg

# Classes
class Hotkey:
    """
    Data class for representing a hotkey and it's action.
    """
    # Constructor
    def __init__(self, keys: Iterable[int], desc: str, callback: Callable[['Hotkey'], None]):
        """
        Initializes a hotkey.

        keys: The DearPyGui key codes that trigger the hotkey. The first key is used as the primary key and must be held down to register further keys.
        desc: A string description of the function of the hotkey to show in the interface.
        callback: The callback function to perform when the hotkey is triggered. Must take a `Hotkey` object as an argument. This will be the defining hotkey object.
        """
        self.keys = keys
        self.desc = desc
        self.callback = callback

    # Python Functions
    def __repr__(self) -> str:
        return f"Hotkey({self.keys}, {self.desc}, {self.callback})"

    def __str__(self) -> str:
        return f"Hotkey({self.keyString()}, {self.desc})"

    # Functions
    def keyString(self, fallback: str = "KEY") -> str:
        """
        Returns the hotkey keys as a string.

        fallback: A string to return if the key code is not recognized.
        """
        return " + ".join([dpgKeyToString(key, fallback=fallback) for key in self.keys])

class HotkeySet:
    """
    Data class for representing a set of hotkeys.
    """
    # Constructor
    def __init__(self, title: str, hotkeys: Iterable[Hotkey]):
        """
        Initializes a hotkey set.

        title: The title of the set as shown in the interface.
        hotkeys: The hotkeys for the set.
        """
        self.title = title
        self.hotkeys = hotkeys

    # Python Functions
    def __repr__(self) -> str:
        return f"HotkeySet({self.title}, {self.hotkeys})"

    def __str__(self) -> str:
        return f"HotkeySet({self.title}, {self.hotkeys})"

    # Functions
    def register(self):
        """
        Registers the hotkeys with the application.
        Should be run within the `dpg.handler_registry` context.
        """
        # Add the hotkeys
        for hotkey in self.hotkeys:
            # Check if the hotkey has multiple keys
            if (len(hotkey.keys) > 1):
                # Add key down handler for the primary key
                dpg.add_key_down_handler(hotkey.keys[0], user_data=hotkey, callback=self.__hotkeyCallback)
            else:
                # Add key release handler for the primary key
                dpg.add_key_release_handler(hotkey.keys[0], user_data=hotkey, callback=self.__hotkeyCallback)

    def definitions(self) -> dict[str, str]:
        """
        Returns the hotkeys for the manager in string format like `{"hotkey": "description"}`.
        """
        # Loop through hotkeys
        return {hotkey.keyString(): hotkey.desc for hotkey in self.hotkeys}

    # Private Functions
    def __hotkeyCallback(self, sender: Union[int, str], keyData: Union[int, list[int, float]], hotkey: Hotkey):
        """
        Callback for when a hotkey is triggered.

        sender: The tag of the sender.
        keyData: The key data as returned by the key handler. If an `int`, it is the key code. If a `list`, it is the key code and the duration the key has been pressed.
        hotkey: The hotkey that was triggered.
        """
        # Check if the other keys are held down
        for key in hotkey.keys[1:]:
            if not dpg.is_key_pressed(key):
                # Exit
                return

        # Call the hotkey's callback
        hotkey.callback(hotkey)

class HotkeyManager:
    """
    Manager class for handling hotkeys.
    """
    # Constants
    _TAG_HOTKEY_REGISTRY = "hotkeyManagerRegistry"

    # Constructor
    def __init__(self, hotkeys: list[HotkeySet]):
        """
        Initializes the hotkey manager.

        hotkeys: A list of `HotkeySet` objects defining the hotkeys.
        """
        self._registered = False
        self._hotkeySets: list[HotkeySet] = hotkeys

    # Functions
    def registerHotkeys(self):
        """
        Registers the hotkeys with the application.
        """
        # Prepare the hotkeys
        with dpg.handler_registry(label="Managed Hotkeys", tag=self._TAG_HOTKEY_REGISTRY):
            # Loop through hotkey sets
            for hotkeySet in self._hotkeySets:
                hotkeySet.register()

        # Mark as registered
        self._registered = True

    def buildToolbar(self):
        """
        Builds the toolbar interface for the hotkeys.
        """
        with dpg.menu(label="Hotkeys"):
            # TODO: Make it look nice in a table
            # Loop through hotkey sets
            setCount = len(self._hotkeySets)
            for i, hotkeySet in enumerate(self._hotkeySets):
                # Add the label
                dpg.add_text(hotkeySet.title)

                # Loop through hotkeys in set
                for keys, desc in hotkeySet.definitions().items():
                    dpg.add_text(f"{keys}: {desc}")

                # Add separator
                if (i < (setCount - 1)):
                    dpg.add_separator()

# Functions
def dpgKeyToString(key: int, fallback: str = "KEY") -> str:
    """
    Converts the given DearPyGui key code to a string.

    key: A DearPyGui key code like `dpg.mvKey_A`.
    fallback: A string to return if the key code is not recognized.

    Returns a string representation of the key code.
    """
    if (key == dpg.mvKey_0): return "0"
    elif (key == dpg.mvKey_1): return "1"
    elif (key == dpg.mvKey_2): return "2"
    elif (key == dpg.mvKey_3): return "3"
    elif (key == dpg.mvKey_4): return "4"
    elif (key == dpg.mvKey_5): return "5"
    elif (key == dpg.mvKey_6): return "6"
    elif (key == dpg.mvKey_7): return "7"
    elif (key == dpg.mvKey_8): return "8"
    elif (key == dpg.mvKey_9): return "9"
    elif (key == dpg.mvKey_A): return "A"
    elif (key == dpg.mvKey_B): return "B"
    elif (key == dpg.mvKey_C): return "C"
    elif (key == dpg.mvKey_D): return "D"
    elif (key == dpg.mvKey_E): return "E"
    elif (key == dpg.mvKey_F): return "F"
    elif (key == dpg.mvKey_G): return "G"
    elif (key == dpg.mvKey_H): return "H"
    elif (key == dpg.mvKey_I): return "I"
    elif (key == dpg.mvKey_J): return "J"
    elif (key == dpg.mvKey_K): return "K"
    elif (key == dpg.mvKey_L): return "L"
    elif (key == dpg.mvKey_M): return "M"
    elif (key == dpg.mvKey_N): return "N"
    elif (key == dpg.mvKey_O): return "O"
    elif (key == dpg.mvKey_P): return "P"
    elif (key == dpg.mvKey_Q): return "Q"
    elif (key == dpg.mvKey_R): return "R"
    elif (key == dpg.mvKey_S): return "S"
    elif (key == dpg.mvKey_T): return "T"
    elif (key == dpg.mvKey_U): return "U"
    elif (key == dpg.mvKey_V): return "V"
    elif (key == dpg.mvKey_W): return "W"
    elif (key == dpg.mvKey_X): return "X"
    elif (key == dpg.mvKey_Y): return "Y"
    elif (key == dpg.mvKey_Z): return "Z"
    elif (key == dpg.mvKey_Back): return "BACK"
    elif (key == dpg.mvKey_Tab): return "TAB"
    elif (key == dpg.mvKey_Clear): return "CLEAR"
    elif (key == dpg.mvKey_Return): return "ENTER"
    elif (key == dpg.mvKey_Shift): return "SHIFT"
    elif (key == dpg.mvKey_Control): return "CTRL"
    elif (key == dpg.mvKey_Alt): return "ALT"
    elif (key == dpg.mvKey_Pause): return "PAUSE"
    elif (key == dpg.mvKey_Capital): return "CAPS"
    elif (key == dpg.mvKey_Escape): return "ESC"
    elif (key == dpg.mvKey_Spacebar): return "SPACE"
    elif (key == dpg.mvKey_Prior): return "PRIOR"
    elif (key == dpg.mvKey_Next): return "NEXT"
    elif (key == dpg.mvKey_End): return "END"
    elif (key == dpg.mvKey_Home): return "HOME"
    elif (key == dpg.mvKey_Left): return "LEFT"
    elif (key == dpg.mvKey_Up): return "UP"
    elif (key == dpg.mvKey_Right): return "RIGHT"
    elif (key == dpg.mvKey_Down): return "DOWN"
    elif (key == dpg.mvKey_Select): return "SELECT"
    elif (key == dpg.mvKey_Print): return "PRINT"
    elif (key == dpg.mvKey_Execute): return "EXEC"
    elif (key == dpg.mvKey_PrintScreen): return "PRINT"
    elif (key == dpg.mvKey_Insert): return "INSERT"
    elif (key == dpg.mvKey_Delete): return "DELETE"
    elif (key == dpg.mvKey_Help): return "HELP"
    elif (key == dpg.mvKey_LWin): return "WIN LEFT"
    elif (key == dpg.mvKey_RWin): return "WIN RIGHT"
    elif (key == dpg.mvKey_Apps): return "APPS"
    elif (key == dpg.mvKey_Sleep): return "SLEEP"
    elif (key == dpg.mvKey_NumPad0): return "NUM 0"
    elif (key == dpg.mvKey_NumPad1): return "NUM 1"
    elif (key == dpg.mvKey_NumPad2): return "NUM 2"
    elif (key == dpg.mvKey_NumPad3): return "NUM 3"
    elif (key == dpg.mvKey_NumPad4): return "NUM 4"
    elif (key == dpg.mvKey_NumPad5): return "NUM 5"
    elif (key == dpg.mvKey_NumPad6): return "NUM 6"
    elif (key == dpg.mvKey_NumPad7): return "NUM 7"
    elif (key == dpg.mvKey_NumPad8): return "NUM 8"
    elif (key == dpg.mvKey_NumPad9): return "NUM 9"
    elif (key == dpg.mvKey_Multiply): return "NUM *"
    elif (key == dpg.mvKey_Add): return "NUM +"
    elif (key == dpg.mvKey_Separator): return "NUM -"
    elif (key == dpg.mvKey_Subtract): return "NUM -"
    elif (key == dpg.mvKey_Decimal): return "NUM ."
    elif (key == dpg.mvKey_Divide): return "NUM /"
    elif (key == dpg.mvKey_F1): return "F1"
    elif (key == dpg.mvKey_F2): return "F2"
    elif (key == dpg.mvKey_F3): return "F3"
    elif (key == dpg.mvKey_F4): return "F4"
    elif (key == dpg.mvKey_F5): return "F5"
    elif (key == dpg.mvKey_F6): return "F6"
    elif (key == dpg.mvKey_F7): return "F7"
    elif (key == dpg.mvKey_F8): return "F8"
    elif (key == dpg.mvKey_F9): return "F9"
    elif (key == dpg.mvKey_F10): return "F10"
    elif (key == dpg.mvKey_F11): return "F11"
    elif (key == dpg.mvKey_F12): return "F12"
    elif (key == dpg.mvKey_F13): return "F13"
    elif (key == dpg.mvKey_F14): return "F14"
    elif (key == dpg.mvKey_F15): return "F15"
    elif (key == dpg.mvKey_F16): return "F16"
    elif (key == dpg.mvKey_F17): return "F17"
    elif (key == dpg.mvKey_F18): return "F18"
    elif (key == dpg.mvKey_F19): return "F19"
    elif (key == dpg.mvKey_F20): return "F20"
    elif (key == dpg.mvKey_F21): return "F21"
    elif (key == dpg.mvKey_F22): return "F22"
    elif (key == dpg.mvKey_F23): return "F23"
    elif (key == dpg.mvKey_F24): return "F24"
    elif (key == dpg.mvKey_F25): return "F25"
    elif (key == dpg.mvKey_NumLock): return "NUM LOCK"
    elif (key == dpg.mvKey_ScrollLock): return "SCROLL LOCK"
    elif (key == dpg.mvKey_LShift): return "LSHIFT"
    elif (key == dpg.mvKey_RShift): return "RSHIFT"
    elif (key == dpg.mvKey_LControl): return "LCTRL"
    elif (key == dpg.mvKey_RControl): return "RCTRL"
    elif (key == dpg.mvKey_LMenu): return "LMENU"
    elif (key == dpg.mvKey_RMenu): return "RMENU"
    elif (key == dpg.mvKey_Browser_Back): return "BROWSER BACK"
    elif (key == dpg.mvKey_Browser_Forward): return "BROWSER FRWD"
    elif (key == dpg.mvKey_Browser_Refresh): return "BROWSER RFSH"
    elif (key == dpg.mvKey_Browser_Stop): return "BROWSER STOP"
    elif (key == dpg.mvKey_Browser_Search): return "BROWSER SRCH"
    elif (key == dpg.mvKey_Browser_Favorites): return "BROWSER FAV"
    elif (key == dpg.mvKey_Browser_Home): return "BROWSER HOME"
    elif (key == dpg.mvKey_Volume_Mute): return "VOLUME MUTE"
    elif (key == dpg.mvKey_Volume_Down): return "VOLUME DOWN"
    elif (key == dpg.mvKey_Volume_Up): return "VOLUME UP"
    elif (key == dpg.mvKey_Media_Next_Track): return "MEDIA NEXT"
    elif (key == dpg.mvKey_Media_Prev_Track): return "MEDIA PREV"
    elif (key == dpg.mvKey_Media_Stop): return "MEDIA STOP"
    elif (key == dpg.mvKey_Media_Play_Pause): return "MEDIA TOGGLE"
    elif (key == dpg.mvKey_Launch_Mail): return "MAIL"
    elif (key == dpg.mvKey_Launch_Media_Select): return "MEDIA SELECT"
    elif (key == dpg.mvKey_Launch_App1): return "APP1"
    elif (key == dpg.mvKey_Launch_App2): return "APP2"
    elif (key == dpg.mvKey_Colon): return ":"
    elif (key == dpg.mvKey_Plus): return "+"
    elif (key == dpg.mvKey_Comma): return ","
    elif (key == dpg.mvKey_Minus): return "-"
    elif (key == dpg.mvKey_Period): return "."
    elif (key == dpg.mvKey_Slash): return "/"
    elif (key == dpg.mvKey_Tilde): return "~"
    elif (key == dpg.mvKey_Open_Brace): return "["
    elif (key == dpg.mvKey_Backslash): return "\\"
    elif (key == dpg.mvKey_Close_Brace): return "]"
    elif (key == dpg.mvKey_Quote): return "\""
    else: return fallback

# Command Line
if __name__ == "__main__":
    print("This file does not contain a command line interface.")
