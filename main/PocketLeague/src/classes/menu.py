import pygame
import PygameXtras as px

from ..files.config import FPS, CENTER
from ..files.colors import DARK_BLUE
from .controller_manager import ControllerManager

class Menu:

    screen: pygame.Surface
    fpsclock: pygame.time.Clock

    def init(screen: pygame.Surface, fpsclock: pygame.time.Clock):
        Menu.screen = screen
        Menu.fpsclock = fpsclock

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
                print("STARTING")

            Menu.screen.fill(DARK_BLUE)
            title.draw()
            start_hint.draw()
            
            pygame.display.flip()
            Menu.fpsclock.tick(FPS)