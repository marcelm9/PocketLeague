import os

# undo windows scaling for this process
if os.name == "nt":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

from demo.game import Demo
Demo.start()