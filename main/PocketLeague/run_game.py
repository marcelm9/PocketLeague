import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.init()

# undo windows scaling for this process
if os.name == "nt":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

from src.menu import Menu
Menu.start()

# from src.game import Game
# Game.debug()
