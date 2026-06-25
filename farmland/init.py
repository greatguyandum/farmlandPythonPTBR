#Init.py

import time
import sys
import winsound
#pip install rich
#pip install playsound3
from playsound3 import playsound
from rich.console import Console
from rich.theme import Theme

character_tags = {
    "alex": "italic green",
    "jake": "bold white",
    "bunnyman": "red",
}


__rich_console = Console(theme=Theme(character_tags))
__rich_theme = Theme()