import pygame

from .files.config import WIN_WIDTH, WIN_HEIGHT, FPS
from .classes.updater import Updater
from .classes.renderer import Renderer

pygame.init()

class Game:

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    fpsclock = pygame.time.Clock()
    Renderer.init(screen)
    
    def start():
        run = True
        i = 0
        while run:
            i += 1
            if i % 120 == 1:
                print("running")
            
            Updater.update()
            Renderer.render()
            
            pygame.display.flip()
            Game.fpsclock.tick(FPS)