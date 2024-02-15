import pygame
import PygameXtras as px

from .files.config import FPS, CENTER, WIN_WIDTH, WIN_HEIGHT
from .files.colors import DARK_BLUE
from .classes.controller_manager import ControllerManager
from .game import Game
from .classes.renderer import Renderer

class Menu:

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), display=2, flags=pygame.FULLSCREEN | pygame.SCALED)
    fpsclock = pygame.time.Clock()
    Renderer.init(screen)
    ControllerManager.init(screen, fpsclock)
    ControllerManager.enough_controllers()
    ControllerManager.declare_controllers()

    def start():

        title = px.Label(
            Menu.screen,
            "Pocket League",
            150,
            CENTER,
            "midbottom",
            f="Comic Sans",
            tc=(240, 240, 240)
        )

        start_hint = px.Label(
            Menu.screen,
            "Press X to start",
            50,
            px.C(CENTER) + px.C(0, 50),
            "midtop",
            f="Comic Sans",
            tc=(240, 240, 240)
        )

        run = True
        while run:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            
            if ControllerManager.someone_pressed_x_or_down():
                Menu.select_player_count()

            Menu.screen.fill(DARK_BLUE)
            title.draw()
            start_hint.draw()
            
            pygame.display.flip()
            Menu.fpsclock.tick(FPS)

    def select_player_count():

        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            
            
            
            pygame.display.flip()
            Menu.fpsclock.tick(FPS)

    def select_teams_names_colors():

        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            
            
            
            pygame.display.flip()
            Menu.fpsclock.tick(FPS)

    def start_game():
        Game.set_config()
        Game.start()
