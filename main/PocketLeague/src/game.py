import pygame

from .files.config import WIN_WIDTH, WIN_HEIGHT, FPS, CENTER, BALL_RADIUS
from .classes.updater import Updater
from .classes.renderer import Renderer
from .classes.field import Field
from .classes.ball_manager import BallManager
from .classes.player import Player

class Game:

    screen: pygame.Surface
    fpsclock: pygame.time.Clock

    def init(screen: pygame.Surface, fpsclock: pygame.time.Clock):
        Game.screen = screen
        Game.fpsclock = fpsclock
        Renderer.init(screen)

    def debug():
        Game.init(
            pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), display=0, flags = pygame.FULLSCREEN | pygame.SCALED),
            pygame.time.Clock()
        )
        Game.start()

    def set_config():
        pass

    def start():
        
        Field.init()
        p1 = Player()
        # p.set_keyboard_input(
        #     up = pygame.K_w,
        #     down = pygame.K_s,
        #     left = pygame.K_a,
        #     right = pygame.K_d,
        #     dash = pygame.K_SPACE
        # )
        p1.set_controller_input(
            controller_index = 0,
            joystick = 0,
            dash_button = 9
        )
        p1.set_pos((300,300))
        p1.set_name("Marcel")
        p1.set_team(0)
        p1.set_color((255,0,0))

        p2 = Player()
        p2.set_controller_input(
            controller_index = 0,
            joystick = 1,
            dash_button = 10
        )
        p2.set_pos((1500,300))
        p2.set_name("Pascal")
        p2.set_team(1)
        p2.set_color((0,255,0))

        BallManager.add_ball(
            CENTER, BALL_RADIUS
        )

        while True:
            
            Updater.update()
            Renderer.render()
            
            pygame.display.flip()
            pygame.display.set_caption(f"fps: {Game.fpsclock.get_fps()}")
