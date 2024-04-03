import pygame

from ..files.config import FPS
from .ball_manager import BallManager
from .player import Player
from .space import Space

class Updater:

    __fpsclock = pygame.time.Clock()

    def update():
        dt = Updater.__fpsclock.tick(FPS)
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        for player in Player.players:
            player.update()

        for ball in BallManager.get_balls():
            ball.update()

        Space.space.step(dt)

        for player in Player.players:
            player.keep_in_bounds()
