import time
import pygame
import PygameXtras as px

from ..classes.controller_manager import ControllerManager
from ..files.colors import SOFT_WHITE
from ..files.config import *


class PlayerSelectionPanel:
    def __init__(self, center, controller_index, controller_input_side: str):
        assert controller_index in [0, 1]
        assert controller_input_side in ["left", "right"]

        self.__controller_index = controller_index
        self.__controller_input_side = controller_input_side

        self.__rect = pygame.Rect(0, 0, *PLAYER_SELECTION_PANEL_SIZE)
        self.__rect.center = center

        self.__no_player_label = px.Label(
            None, "No player", 40, center, tc=SOFT_WHITE, f="Comic Sans"
        )

        self.__active = False
        self.__active_time_start: float # avoids unintentionally setting self as ready when joining lobby
        self.__ready = False

        # lets also show the player how they would look like in game (as first thing of the panel, above the name)
        labels = ("Name", "Team", "Color", "Boost", "Goal Explosion")

        self.__possible_values = [
            NAMES,
            TEAM_NAMES,
            COLOR_NAMES,
            BOOST_TYPES,
            GOAL_EXPLOSION_TYPES,
        ]

        self.__indexes = [0, 0, 0, 0, 0]

        self.__max_indexes = [len(item) - 1 for item in self.__possible_values]

        self.__current_index = 0

        start = 120
        jump = 130

        self.__labels = [
            px.Label(
                None,
                item,
                20,
                self.__offset((PLAYER_SELECTION_PANEL_SIZE[0] // 2, start + jump * i)),
                tc=SOFT_WHITE,
                f="Comic Sans",
            )
            for i, item in enumerate(labels)
        ]

        self.__choice_labels = [
            px.Label(
                None,
                self.__possible_values[i][self.__indexes[i]],
                40,
                self.__offset(
                    (
                        PLAYER_SELECTION_PANEL_SIZE[0] // 2,
                        start + (jump / 2.5) + jump * i,
                    )
                ),
                tc=SOFT_WHITE,
                f="Comic Sans",
                bc=SOFT_WHITE,
                fd=(PLAYER_SELECTION_PANEL_SIZE[0] // 1.15, 70),
                br=10,
            )
            for i in range(len(self.__labels))
        ]

        self.__ready_label = px.Label(
            None,
            "not ready",
            30,
            (center[0], start + jump * (len(self.__choice_labels) + 1) - 10),
            tc=SOFT_WHITE,
            f="Comic Sans",
            fd=(PLAYER_SELECTION_PANEL_SIZE[0] // 1.5, 55),
            br=15
        )

    def __offset(self, pos):
        return (self.__rect[0] + pos[0], self.__rect[1] + pos[1])

    def __update_labels(self):
        if self.__ready:
            self.__ready_label.update_text("ready")
            self.__ready_label.update_colors(
                backgroundcolor=(0,150,0)
            )
        else:
            self.__ready_label.update_text("not ready")
            self.__ready_label.update_colors(
                backgroundcolor=(150,0,0)
            )
        for i in range(len(self.__choice_labels)):
            self.__choice_labels[i].update_text(
                self.__possible_values[i][self.__indexes[i]]
            )
            if i == self.__current_index:
                self.__choice_labels[i].update_borderwidth(3)
            else:
                self.__choice_labels[i].update_borderwidth(0)

    def update(self):
        keys = ControllerManager.get_pressed_by(
            self.__controller_index, self.__controller_input_side
        )
        if not self.__active:
            if keys[0]:
                self.__active = True
                self.__update_labels()
                self.__active_time_start = time.time()

            if keys[5]:
                return False

        if self.__active:
            if keys[0] and (time.time() - self.__active_time_start) > 1:
                self.__ready = not self.__ready
            if keys[1]:
                self.__current_index = max(0, self.__current_index - 1)
            elif keys[2]:
                self.__current_index = min(
                    len(self.__choice_labels) - 1, self.__current_index + 1
                )
            if keys[3]:
                self.__indexes[self.__current_index] = max(
                    0, self.__indexes[self.__current_index] - 1
                )
            elif keys[4]:
                self.__indexes[self.__current_index] = min(
                    self.__max_indexes[self.__current_index],
                    self.__indexes[self.__current_index] + 1,
                )
            
            if keys[5]:
                self.__active = False
                self.__ready = False

            if any(keys):
                self.__update_labels()

    def draw(self, surface):
        if self.__active:
            for label in self.__labels:
                label.draw_to(surface)
            for label in self.__choice_labels:
                label.draw_to(surface)
            pygame.draw.circle(
                surface,
                TEAM_COLOR_MAP[self.__possible_values[1][self.__indexes[1]]],
                self.__offset(PLAYER_SELECTION_PANEL_PREVIEW_OFFSET),
                PLAYER_OUTER_RADIUS,
            )
            pygame.draw.circle(
                surface,
                COLOR_MAP[self.__possible_values[2][self.__indexes[2]]],
                self.__offset(PLAYER_SELECTION_PANEL_PREVIEW_OFFSET),
                PLAYER_INNER_RADIUS,
            )
            self.__ready_label.draw_to(surface)
        else:
            self.__no_player_label.draw_to(surface)
        pygame.draw.rect(surface, SOFT_WHITE, self.__rect, 5, 30)
