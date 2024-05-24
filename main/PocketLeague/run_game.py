import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

pygame.init()

# undo windows scaling for this process
if os.name == "nt":
    import ctypes

    ctypes.windll.shcore.SetProcessDpiAwareness(1)

from src.ui.menu import Menu

pygame.mouse.set_cursor(
    (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0)
)

Menu.start()
