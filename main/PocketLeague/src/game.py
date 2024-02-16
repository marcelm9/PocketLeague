import pygame

from .files.config import WIN_WIDTH, WIN_HEIGHT, FPS
from .classes.updater import Updater
from .classes.renderer import Renderer
from .classes.field import Field

class Game:

    screen: pygame.Surface
    fpsclock: pygame.time.Clock

    def init(screen: pygame.Surface, fpsclock: pygame.time.Clock):
        Game.screen = screen
        Game.fpsclock = fpsclock
        Renderer.init(screen)

    def debug():
        Game.init(
            pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), flags = pygame.FULLSCREEN | pygame.SCALED),
            pygame.time.Clock()
        )
        Game.start()

    def set_config():
        pass

    def start():
        
        Field.init()

        while True:
            
            Updater.update()
            Renderer.render()
            
            pygame.display.flip()
            Game.fpsclock.tick(FPS)
