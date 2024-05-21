import pygame
import PygameXtras as px
from PygameXtras import PSVG

from ..classes.controller_manager import ControllerManager
from ..classes.player_config_manager import PlayerConfigManager
from ..files.colors import DARK_BLUE, ERROR_LABEL_COLOR, SOFT_WHITE
from ..files.config import *
from ..game import Game
from .player_selection_panel import PlayerSelectionPanel

PSVG.set_size(BUTTON_DRAWER_SIZE)
PSVG.set_linewidth(BUTTON_DRAWER_LINE_WIDTH)


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
            190,
            CENTER,
            "midbottom",
            f="Comic Sans",
            tc=(240, 240, 240),
        )

        start_label = px.Label(
            Menu.screen,
            "Start a match",
            50,
            px.C(CENTER) + px.C(0, 50),
            "midtop",
            f="Comic Sans",
            tc=SOFT_WHITE,
        )

        garage_label = px.Label(
            Menu.screen,
            "Visit the garage",
            50,
            px.C(CENTER) + px.C(0, 150),
            "midtop",
            f="Comic Sans",
            tc=SOFT_WHITE,
        )

        error_labels = []

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
                    elif event.key == pygame.K_SPACE:
                        PlayerConfigManager._use_debug_configs()

            keys = ControllerManager.get_pressed_by_everyone()
            if keys[3]:
                if len(errors := PlayerConfigManager.get_errors()) == 0:
                    Menu.match_config()
                    error_labels.clear()
                else:
                    error_labels.clear()
                    for i, error in enumerate(errors):
                        error_labels.append(
                            px.Label(
                                Menu.screen,
                                error,
                                40,
                                (CENTER[0], garage_label.bottom + 70 + 80 * i),
                                f="Comic Sans",
                                tc=ERROR_LABEL_COLOR,
                            )
                        )
            elif keys[1]:
                Menu.player_config()
                error_labels.clear()

            Menu.screen.fill(DARK_BLUE)
            title.draw()
            start_label.draw()
            garage_label.draw()
            PSVG.left(Menu.screen, (start_label.left - 200, start_label.center[1]))
            PSVG.slash(Menu.screen, (start_label.left - 130, start_label.center[1]))
            PSVG.square(Menu.screen, (start_label.left - 60, start_label.center[1]))
            PSVG.up(Menu.screen, (garage_label.left - 200, garage_label.center[1]))
            PSVG.slash(Menu.screen, (garage_label.left - 130, garage_label.center[1]))
            PSVG.triangle(Menu.screen, (garage_label.left - 60, garage_label.center[1]))
            for e_label in error_labels:
                e_label.draw()

            pygame.display.flip()
            Menu.fpsclock.tick(60)

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
        current_index = 1

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

            keys = ControllerManager.get_pressed_by_everyone()
            if current_index == 0 and keys[0]:
                return
            elif current_index == 4 and keys[0]:
                Game.start()
            elif keys[1]:
                current_index = max(0, min(4, current_index - 1))
            elif keys[2]:
                current_index = max(0, min(4, current_index + 1))
            elif 1 <= current_index <= 3:
                if keys[3]:
                    value_indexes[current_index - 1] = max(
                        0, value_indexes[current_index - 1] - 1
                    )
                    update_value_labels()
                elif keys[4]:
                    value_indexes[current_index - 1] = min(
                        value_indexes_max[current_index - 1],
                        value_indexes[current_index - 1] + 1,
                    )
                    update_value_labels()

            for i, label in enumerate([back_button, *value_labels, confirm_button]):
                if current_index == i:
                    label.update_borderwidth(3)
                else:
                    label.update_borderwidth(0)

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

        panels: list[PlayerSelectionPanel] = [
            PlayerSelectionPanel(PLAYER_SELECTION_PANEL_POSITIONS[0], 0, "left"),
            PlayerSelectionPanel(PLAYER_SELECTION_PANEL_POSITIONS[1], 0, "right"),
            PlayerSelectionPanel(PLAYER_SELECTION_PANEL_POSITIONS[2], 1, "left"),
            PlayerSelectionPanel(PLAYER_SELECTION_PANEL_POSITIONS[3], 1, "right"),
        ]

        panels[0].set_from_player_config(
            PlayerConfigManager.get_by_controller(0, "left")
        )
        panels[1].set_from_player_config(
            PlayerConfigManager.get_by_controller(0, "right")
        )
        panels[2].set_from_player_config(
            PlayerConfigManager.get_by_controller(1, "left")
        )
        panels[3].set_from_player_config(
            PlayerConfigManager.get_by_controller(1, "right")
        )

        save_label = px.Label(
            Menu.screen,
            "Save",
            40,
            (CENTER[0] + 50, Menu.screen.get_height() - 50),
            "midbottom",
            tc=SOFT_WHITE,
            f="Comic Sans",
        )

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

            ControllerManager.update()
            for p in panels:
                p.update()

            if ControllerManager.has_anyone_pressed_ps_button():
                PlayerConfigManager.clear_players()
                active_panels = [p for p in panels if p.is_active()]
                for p in active_panels:
                    PlayerConfigManager.add_player(p.get_player_config())
                return

            Menu.screen.fill(DARK_BLUE)
            for p in panels:
                p.draw(Menu.screen)
            save_label.draw()
            PSVG.ps(Menu.screen, (save_label.left - 65, save_label.center[1] + 6))

            pygame.display.flip()
            Menu.fpsclock.tick(10)

    def start_game():
        Game.set_config()
        Game.start()
