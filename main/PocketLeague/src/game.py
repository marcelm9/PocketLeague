import pygame

from .files.config import WIN_WIDTH, WIN_HEIGHT, FPS
from .classes.updater import Updater
from .classes.renderer import Renderer
from .classes.menu import Menu
from .classes.controller_manager import ControllerManager

pygame.init()

class Game:

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), display=2, flags=pygame.FULLSCREEN | pygame.SCALED)
    fpsclock = pygame.time.Clock()
    Renderer.init(screen)
    ControllerManager.init(screen, fpsclock)
    
    def start():

        ControllerManager.enough_controllers()
        ControllerManager.declare_controllers()

        Menu.init(Game.screen, Game.fpsclock)
        Menu.start()

    def run_game():

        while True:
            
            Updater.update()
            Renderer.render()
            
            pygame.display.flip()
            Game.fpsclock.tick(FPS)
