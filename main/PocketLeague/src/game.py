import pygame

from .files.config import WIN_WIDTH, WIN_HEIGHT, FPS
from .classes.updater import Updater
from .classes.renderer import Renderer
from .classes.field import Field
from .classes.ball_manager import BallManager

class Game:

    screen: pygame.Surface
    fpsclock: pygame.time.Clock

    def init(screen: pygame.Surface, fpsclock: pygame.time.Clock):
        Game.screen = screen
        Game.fpsclock = fpsclock
        Renderer.init(screen)

    def debug():
        Game.init(
            pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), display=2, flags = pygame.FULLSCREEN | pygame.SCALED),
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
            pygame.display.set_caption(f"fps: {Game.fpsclock.get_fps()}")
