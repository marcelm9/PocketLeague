import os

# undo windows scaling for this process
if os.name == "nt":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

from src.game import Game
Game.start()
