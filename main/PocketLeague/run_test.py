import os
import random

import pygame
from src.classes.match_stats import MatchStats
from src.classes.player_config_manager import PlayerConfigManager
from src.files.config import *
from src.ui.after_match_screen import AfterMatchScreen

pygame.init()

# undo windows scaling for this process
if os.name == "nt":
    import ctypes

    ctypes.windll.shcore.SetProcessDpiAwareness(1)


screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
fpsclock = pygame.time.Clock()
AfterMatchScreen.init(fpsclock, screen)
teams = ["Team Blue" for _ in range(3)] + ["Team Orange" for _ in range(3)]
players = [(NAMES[i], teams.pop(random.randint(0, len(teams) - 1))) for i in range(4)]
PlayerConfigManager._inject_test(players)
MatchStats._inject_test(players)
AfterMatchScreen.show()
