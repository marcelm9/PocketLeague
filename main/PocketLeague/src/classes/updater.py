import pygame
from .ball_manager import BallManager
from .player import Player

class Updater:
    def update():
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


