import pygame
from .point_manager import PointManager

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
                elif event.key == pygame.K_SPACE:
                    PointManager.clear()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                PointManager.add_point(
                    event.pos
                )
