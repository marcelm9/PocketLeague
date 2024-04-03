import pygame

from .files.config import WIN_WIDTH, WIN_HEIGHT, FPS, CENTER, BALL_RADIUS
from .classes.updater import Updater
from .classes.renderer import Renderer
from .classes.field import Field
from .classes.ball_manager import BallManager
from .classes.player import Player
from .classes.HUD import HUD

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
        p = Player()
        p.set_keyboard_input(
             up = pygame.K_w,
             down = pygame.K_s,
             left = pygame.K_a,
             right = pygame.K_d,
             dash = pygame.K_SPACE
         )
        #p.set_controller_input(
         #   controller_index = 0,
          #  joystick = 0,
           # dash_button = 9
        #)
        p.set_pos((300,300))
        p.set_name("Marcel")
        p.set_team(0)
        p.set_color((255,0,0))

        
        p2 = Player()
        p2.set_keyboard_input(
             up = pygame.K_w,
             down = pygame.K_s,
             left = pygame.K_a,
             right = pygame.K_d,
             dash = pygame.K_SPACE
         )
        #p.set_controller_input(
         #   controller_index = 0,
          #  joystick = 0,
           # dash_button = 9
        #)
        p2.set_pos((400,400))
        p2.set_name("PauliGOAT")
        p2.set_team(0)
        p2.set_color((255,0,255))

        p3 = Player()
        p3.set_keyboard_input(
             up = pygame.K_w,
             down = pygame.K_s,
             left = pygame.K_a,
             right = pygame.K_d,
             dash = pygame.K_SPACE
         )
        #p.set_controller_input(
         #   controller_index = 0,
          #  joystick = 0,
           # dash_button = 9
        #)
        p3.set_pos((400,400))
        p3.set_name("Monke")
        p3.set_team(1)
        p3.set_color((20,255,0))

        p4 = Player()
        p4.set_keyboard_input(
             up = pygame.K_w,
             down = pygame.K_s,
             left = pygame.K_a,
             right = pygame.K_d,
             dash = pygame.K_SPACE
         )
        #p.set_controller_input(
         #   controller_index = 0,
          #  joystick = 0,
           # dash_button = 9
        #)
        p4.set_pos((400,400))
        p4.set_name("Brrrrr")
        p4.set_team(1)
        p4.set_color((255,255,0))


        HUD.init(Game.screen)

        BallManager.add_ball(
            CENTER, (0,0), BALL_RADIUS
        )

        while True:
            
            Updater.update()
            Renderer.render()
            
            pygame.display.flip()
            Game.fpsclock.tick(FPS)
            pygame.display.set_caption(f"fps: {Game.fpsclock.get_fps()}")
