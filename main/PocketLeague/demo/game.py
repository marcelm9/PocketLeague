import pygame

from .updater import Updater
from .renderer import Renderer

class Demo:

    screen = pygame.display.set_mode((500, 500))
    fpsclock = pygame.time.Clock()
    Renderer.init(screen)

    def start():
        run = True
        while run:
            
            Updater.update()
            Renderer.render()
            
            pygame.display.flip()
            Demo.fpsclock.tick(60)
