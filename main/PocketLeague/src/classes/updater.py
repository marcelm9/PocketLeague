import pygame
from .ball_manager import BallManager

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    BallManager.add_ball(event.pos, (-1, -1), 5, 10)
                elif event.button == 3:
                    BallManager.add_ball(event.pos, (1, -1), 5, 10)


        for ball in BallManager.get_balls():
            ball.update()


