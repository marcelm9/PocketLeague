import pygame
import PygameXtras as px

from .player_selection_panel import PlayerSelectionPanel

from ..files.config import *
from ..files.colors import DARK_BLUE, SOFT_WHITE
from ..classes.controller_manager import ControllerManager
from ..game import Game


class Menu:

    screen = pygame.display.set_mode(
        (WIN_WIDTH, WIN_HEIGHT), display=0, flags=pygame.FULLSCREEN | pygame.SCALED
    )
    fpsclock = pygame.time.Clock()
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
            tc=(240, 240, 240),
        )

        start_hint = px.Label(
            Menu.screen,
            "Press X to start",
            50,
            px.C(CENTER) + px.C(0, 50),
            "midtop",
            f="Comic Sans",
            tc=(240, 240, 240),
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
                Menu.match_config()

            # debug
            Menu.match_config()

            Menu.screen.fill(DARK_BLUE)
            title.draw()
            start_hint.draw()

            pygame.display.flip()
            Menu.fpsclock.tick(FPS)

    def match_config():
        labels = []
        options = ("Map", "Duration (seconds)", "Boost allowed")
        for i, text in enumerate(options):
            labels.append(
                px.Label(
                    Menu.screen,
                    text,
                    40,
                    (600, 400 + 80 * i),
                    "topleft",
                    f=HUD_FONT,
                    tc=SOFT_WHITE,
                    fh=80,
                )
            )

        possible_values = [
            ["Default map"],
            [i for i in range(60, 301, 30)],
            [True, False],
        ]
        value_indexes_max = [
            len(possible_values[i]) - 1 for i in range(len(possible_values))
        ]
        value_indexes = [0, 2, 0]  # default values

        value_labels = []
        for i in range(len(options)):
            value_labels.append(
                px.Label(
                    Menu.screen,
                    possible_values[i][value_indexes[i]],
                    40,
                    (1100, 400 + 80 * i),
                    "topleft",
                    f=HUD_FONT,
                    tc=SOFT_WHITE,
                    fh=80,
                    fw=300,
                    bc=SOFT_WHITE,
                    br=5,
                )
            )

        def update_value_labels():
            i = 0
            for value_index, label in zip(value_indexes, value_labels):
                label.update_text(possible_values[i][value_index])
                i += 1

        back_button = px.Label(
            Menu.screen,
            "Back",
            40,
            (500, 300),
            f=HUD_FONT,
            tc=SOFT_WHITE,
            xad=20,
            yad=10,
            bc=SOFT_WHITE,
            br=10,
        )

        confirm_button = px.Label(
            Menu.screen,
            "Confirm",
            40,
            (1400, 730),
            f=HUD_FONT,
            tc=SOFT_WHITE,
            xad=20,
            yad=10,
            bc=SOFT_WHITE,
            br=10,
        )

        # different index than in lines above !
        current_index = 0

        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # return
                        # debug
                        pygame.quit()
                        exit()

            keys = ControllerManager.get_pressed_by_everyone()
            if current_index == 0 and keys[0]:
                return
            elif current_index == 4 and keys[0]:
                Menu.player_config()
            elif keys[1]:
                current_index = max(0, min(4, current_index - 1))
            elif keys[2]:
                current_index = max(0, min(4, current_index + 1))
            elif 1 <= current_index <= 3:
                if keys[3]:
                    value_indexes[current_index - 1] = max(
                        0,
                        min(
                            value_indexes_max[current_index - 1],
                            value_indexes[current_index - 1] - 1,
                        ),
                    )
                    update_value_labels()
                elif keys[4]:
                    value_indexes[current_index - 1] = max(
                        0,
                        min(
                            value_indexes_max[current_index - 1],
                            value_indexes[current_index - 1] + 1,
                        ),
                    )
                    update_value_labels()

            for i, label in enumerate([back_button, *value_labels, confirm_button]):
                if current_index == i:
                    label.update_borderwidth(3)
                else:
                    label.update_borderwidth(0)

            # debug
            Menu.player_config()

            Menu.screen.fill(DARK_BLUE)
            for label in labels + value_labels:
                label.draw()
            back_button.draw()
            confirm_button.draw()

            pygame.display.flip()
            Menu.fpsclock.tick(10)

    def player_config():

        # i want players to be able to join in sporadically
        # this also makes it easier for two players to play on seperate controllers

        panels: list[PlayerSelectionPanel] = [None, None, None, None]
        panels[0] = PlayerSelectionPanel(PLAYER_SELECTION_PANEL_POSITIONS[0], 0, "left")
        panels[1] = PlayerSelectionPanel(PLAYER_SELECTION_PANEL_POSITIONS[1], 0, "right")
        panels[2] = PlayerSelectionPanel(PLAYER_SELECTION_PANEL_POSITIONS[2], 1, "left")
        panels[3] = PlayerSelectionPanel(PLAYER_SELECTION_PANEL_POSITIONS[3], 1, "right")

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

            for p in panels:
                p.update()

            Menu.screen.fill(DARK_BLUE)
            for p in panels:
                p.draw(Menu.screen)

            pygame.display.flip()
            Menu.fpsclock.tick(10)

    def start_game():
        Game.set_config()
        Game.start()
