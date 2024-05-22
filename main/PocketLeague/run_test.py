import os
import random
from PocketLeague.src.classes.match_stats import MatchStats
from PocketLeague.src.classes.player_config_manager import PlayerConfigManager
from PocketLeague.src.files.config import *
import pygame
pygame.init()

# undo windows scaling for this process
if os.name == "nt":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

from PocketLeague.src.ui.after_match_screen import AfterMatchScreen

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
fpsclock = pygame.time.Clock()
AfterMatchScreen.init(fpsclock, screen)
teams = ["Team Blue" for _ in range(3)] + ["Team Orange" for _ in range(3)]
players = [
    (NAMES[i], teams.pop(random.randint(0, len(teams) - 1))) for i in range(3)
]
PlayerConfigManager._inject_test(players)
MatchStats._inject_test(players)
AfterMatchScreen.show()
